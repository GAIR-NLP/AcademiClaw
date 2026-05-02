#include <Arduino.h>
#include "FastIMU.h"
#include <Wire.h>
#include "soc/timer_group_struct.h"
#include "soc/timer_group_reg.h"
#include "Yukino-project-1_inferencing.h"
#include <BluetoothSerial.h>

void QMI8658setup();
static bool debug_nn = false; // Set this to true to see e.g. features generated from the raw signal
#define IMU_ADDRESS 0x6a      // Change to the address of the IMU
// #define PERFORM_CALIBRATION //Comment to disable startup calibration
QMI8658 IMU; // Change to the name of any supported IMU!
byte step = 0;
// Currently supported IMUS: MPU9255 MPU9250 MPU6886 MPU6500 MPU6050 ICM20689 ICM20690 BMI055 BMX055 BMI160 LSM6DS3 LSM6DSL QMI8658
#define BufferSize EI_CLASSIFIER_RAW_SAMPLE_COUNT * 2
calData calib = {0};             // Calibration data
AccelData accelData[BufferSize]; // Sensor data
GyroData gyroData[BufferSize];
int16_t curPos = 0;
MagData magData;

hw_timer_t *timer = NULL;
SemaphoreHandle_t sem;

//蓝牙处理
BluetoothSerial SerialBT;
int buttonPin = 35;  // 蓝牙按键连接到35
String targetDevice = "ESP32_B";  // 目标设备名称，即 ESP32 B 的名称
bool isConnected = false;


void ARDUINO_ISR_ATTR timeoutCb()
{
  BaseType_t higherTaskWoken = pdFALSE;
  if (step == 1)
    xSemaphoreGiveFromISR(sem, &higherTaskWoken);
  if (higherTaskWoken)
  {
    portYIELD_FROM_ISR();
  }

  //
  // if (higherTaskWoken) {
  //     portYIELD_FROM_ISR();
  // }
}

void setup()
{
  Serial.begin(115200);
  QMI8658setup();
  /* 初始化定时器 */

  sem = xSemaphoreCreateBinary();
  timer = timerBegin(0, 80, true); // 时钟频率 = 80MHz / 80 = 1MHz
  timerAttachInterrupt(timer, timeoutCb, false);
  timerAlarmWrite(timer, 10000, true); // 闹钟频率 = (1 / 1MHz) * 1000000 = 1s
  step = 0;                            // 等待状态
  pinMode(34, INPUT);
  pinMode(2, OUTPUT);
  curPos = 0;
  // timerAlarmEnable(timer);

  //蓝牙处理
  pinMode(buttonPin, INPUT);  // 按键输入
  SerialBT.begin("ESP32_A");  // 设置本设备名称
  ei_printf("The device started, now you can pair it with bluetooth!");

  // 启用主机模式
    if (!SerialBT.begin("ESP32_A", true)) {
        Serial.println("Failed to start Bluetooth in Master mode");
        return;
    }
    Serial.println("Bluetooth started in Master mode. Ready to connect!");

  while (digitalRead(buttonPin) == HIGH) {
    // 等待按键按下启动蓝牙
    delay(100);
  }
  bool connected = false;

  connected=SerialBT.connect(targetDevice);  // 连接目标设备

  if(connected){
    ei_printf("Connected successfully!");
    isConnected = true;
  }
}


// Allocate a buffer here for the values we'll read from the IMU
float buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE * 2] = {0};
void loop()
{
  if (step == 0)
  {
    if (digitalRead(34) == 0)
    {
      while (digitalRead(34) == 0)
        delay(10); // 按键1按下，等待弹起
      step = 1;
      curPos = 0;
      digitalWrite(2, HIGH); // 打开指示灯
      timerAlarmEnable(timer);
    }
  }
  else if (step == 1)
  {

    if (pdTRUE == xSemaphoreTake(sem, portMAX_DELAY))
    {

      IMU.update();
      IMU.getAccel(&accelData[curPos]);
      IMU.getGyro(&gyroData[curPos++]);
      if (curPos >= BufferSize)
      {
        step = 2;                 // 串口输出所有采集的数据
        timerAlarmDisable(timer); // 关闭定时器
      }
    }
  }
  else if (step == 2)
  {
    // 串口输出采集的数据 10秒
    step = 0;
    digitalWrite(2, LOW); // 关闭指示灯
    for (int i = 0; i < BufferSize; i++)
    {
      /*Serial.print(accelData[i].accelX);
      Serial.print("\t");
      Serial.print(accelData[i].accelY);
      Serial.print("\t");
      Serial.print(accelData[i].accelZ);
      Serial.print("\t");
      Serial.print(gyroData[i].gyroX);
      Serial.print("\t");
      Serial.print(gyroData[i].gyroY);
      Serial.print("\t");
      Serial.print(gyroData[i].gyroZ);
      Serial.println();*/
      buffer[6 * i + 0] = accelData[i].accelX;
      buffer[6 * i + 1] = accelData[i].accelY;
      buffer[6 * i + 2] = accelData[i].accelZ;
      buffer[6 * i + 3] = gyroData[i].gyroX;
      buffer[6 * i + 4] = gyroData[i].gyroY;
      buffer[6 * i + 5] = gyroData[i].gyroZ;
    }

    // Turn the raw buffer in a signal which we can the classify
    int count = 0;
    for (int index = 0; index < 600; index += 60)
    {
      signal_t signal;
      
      int err = numpy::signal_from_buffer(&buffer[index], EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, &signal);
      if (err != 0)
      {
        ei_printf("Failed to create signal from buffer (%d)\n", err);
        return;
      }

      // Run the classifier
      ei_impulse_result_t result = {0};

      err = run_classifier(&signal, &result, debug_nn);
      if (err != EI_IMPULSE_OK)
      {
        ei_printf("ERR: Failed to run classifier (%d)\n", err);
        return;
      }

      // print the predictions
      
      if(count == 0){
        ei_printf("Predictions ");
        ei_printf("(DSP: %d ms., Classification: %d ms., Anomaly: %d ms.)",
                result.timing.dsp, result.timing.classification, result.timing.anomaly);
        ei_printf(": \n");
        for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++)
        {
          ei_printf("    %s: %.5f\n", result.classification[ix].label, result.classification[ix].value);
        }

        //取最高概率的标签，发送蓝牙指令
        if(isConnected){
          float max = 0;
          String label = "";
          for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++)
          {
            if (result.classification[ix].value > max)
            {
              max = result.classification[ix].value;
              label = result.classification[ix].label;
            }
          }

          if(label == "Forward") SerialBT.println("1");
          else if(label == "Backward") SerialBT.println("2");
          else if(label == "Leftward") SerialBT.println("3");
          else if(label == "Rightward") SerialBT.println("4");
        }
        count++;
      }
    }
  }
}

void QMI8658setup()
{
  Wire.begin(32, 33);
  Wire.setClock(400000); // 400khz clock

  int err = IMU.init(calib, IMU_ADDRESS);
  if (err != 0)
  {
    Serial.print("Error initializing IMU: ");
    Serial.println(err);
    while (true)
    {
      ;
    }
  }

#ifdef PERFORM_CALIBRATION
  Serial.println("FastIMU calibration & data example");
  if (IMU.hasMagnetometer())
  {
    delay(1000);
    Serial.println("Move IMU in figure 8 pattern until done.");
    delay(3000);
    IMU.calibrateMag(&calib);
    Serial.println("Magnetic calibration done!");
  }
  else
  {
    delay(5000);
  }

  delay(5000);
  Serial.println("Keep IMU level.");
  delay(5000);
  IMU.calibrateAccelGyro(&calib);
  Serial.println("Calibration done!");
  Serial.println("Accel biases X/Y/Z: ");
  Serial.print(calib.accelBias[0]);
  Serial.print(", ");
  Serial.print(calib.accelBias[1]);
  Serial.print(", ");
  Serial.println(calib.accelBias[2]);
  Serial.println("Gyro biases X/Y/Z: ");
  Serial.print(calib.gyroBias[0]);
  Serial.print(", ");
  Serial.print(calib.gyroBias[1]);
  Serial.print(", ");
  Serial.println(calib.gyroBias[2]);
  delay(5000);
  IMU.init(calib, IMU_ADDRESS);
#endif

  // err = IMU.setGyroRange(500);      //USE THESE TO SET THE RANGE, IF AN INVALID RANGE IS SET IT WILL RETURN -1
  // err = IMU.setAccelRange(2);       //THESE TWO SET THE GYRO RANGE TO ±500 DPS AND THE ACCELEROMETER RANGE TO ±2g

  if (err != 0)
  {
    Serial.print("Error Setting range: ");
    Serial.println(err);
    while (true)
    {
      ;
    }
  }
}

void QMI8658loop()
{

  // Serial.print(accelData.accelX);
  // Serial.print("\t");
  // Serial.print(accelData.accelY);
  // Serial.print("\t");
  // Serial.print(accelData.accelZ);
  // Serial.print("\t");

  // Serial.print(gyroData.gyroX);
  // Serial.print("\t");
  // Serial.print(gyroData.gyroY);
  // Serial.print("\t");
  // Serial.print(gyroData.gyroZ);
  // if (IMU.hasMagnetometer()) {
  //   IMU.getMag(&magData);
  //   Serial.print("\t");
  //   Serial.print(magData.magX);
  //   Serial.print("\t");
  //   Serial.print(magData.magY);
  //   Serial.print("\t");
  //   Serial.print(magData.magZ);
  // }
  // if (IMU.hasTemperature()) {
  //   Serial.print("\t");
  //   Serial.println(IMU.getTemp());
  // }
  // else {
  //   Serial.println();
  // }
  delay(50);
}
