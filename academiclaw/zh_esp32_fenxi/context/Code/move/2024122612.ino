#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>
#include <SPI.h>
#include <TJpg_Decoder.h>
#include <Arduino.h>
#include "image_bitmaps.h"

// 定义屏幕的引脚配置和屏幕尺寸
#define TFT_CS        10 // Chip select pin
#define TFT_RST       9  // Reset pin
#define TFT_DC        8  // Data/command pin

// 屏幕分辨率
#define TFT_WIDTH     128
#define TFT_HEIGHT    128

Adafruit_ST7735 tft = Adafruit_ST7735(5, 21, 23, 18, 0);


//Initializing Motor Pin 
int motorA1pin = 17; //左轮电机Motor1A 
int motorB1pin = 22; //左轮电机Motor1B 
 
int motorA2pin = 4; //右轮电机Motor2A 
int motorB2pin = 16; //右轮电机Motor2B 
int speed=100; 
int running_time=2000;
 
// 蓝牙设置
BluetoothSerial SerialBT;
String receivedData = "";


void setup() { 

  // 初始化串口
  Serial.begin(115200);

  pinMode(2,OUTPUT);

  // 初始化蓝牙
  SerialBT.begin("ESP32_B");
  Serial.println("Waiting for connection from ESP32 A...");

  digitalWrite(2,HIGH);
  // 等待蓝牙客户端连接
  while (!SerialBT.hasClient()) {
    delay(1000);
    Serial.println("Waiting for client...");
  }
  Serial.println("Client connected!");

  // 初始化 ST7735 显示屏
  tft.initR(INITR_BLACKTAB);  // 初始化为 ST7735 黑色板
  tft.setRotation(1);        // 设置屏幕方向
  tft.fillScreen(ST77XX_BLACK);  // 清空屏幕

  //Declaring Motor pin as output 
  pinMode(motorA1pin, OUTPUT); 
  pinMode(motorB1pin, OUTPUT); 
 
  pinMode(motorA2pin, OUTPUT); 
  pinMode(motorB2pin, OUTPUT); 
} 
//小车前进,持续1s 
void forward_moving()//只有左轮向后转
{
  digitalWrite(motorB1pin,LOW); 
  digitalWrite(motorB2pin,LOW); 
  analogWrite(motorA1pin, speed); 
  analogWrite(motorA2pin, speed); 
  delay(running_time);
} 
//小车后退,持续1s 
void backward_moving()//两轮向后转
{
  digitalWrite(motorB1pin,HIGH); 
  digitalWrite(motorB2pin,HIGH); 
  analogWrite(motorA1pin, speed); 
  analogWrite(motorA2pin, speed); 
  delay(running_time);
}
//小车右转,持续1s 
void rightward_moving()//只有左轮向后转
{
  digitalWrite(motorB1pin,LOW); 
  digitalWrite(motorB2pin,HIGH); 
  analogWrite(motorA1pin, speed); 
  analogWrite(motorA2pin, speed); 
  delay(running_time/2); 
}
//小车左转,持续1s 
void leftward_moving()//只有右轮向后转
{
  digitalWrite(motorB1pin,HIGH); 
  digitalWrite(motorB2pin,LOW); 
  analogWrite(motorA1pin, speed); 
  analogWrite(motorA2pin, speed); 
  delay(running_time/2); 
}
void stop()
{
  digitalWrite(motorB1pin,LOW); 
  digitalWrite(motorB2pin,LOW); 
  analogWrite(motorA1pin, 0); 
  analogWrite(motorA2pin, 0); 
  delay(running_time); 
}

// 更新显示屏内容
void updateDisplay(String data) {
  if (data == "1") {
    // 显示第一张图片
    displayImage(1);
    Serial.println("Displaying image 1");
  } else if (data == "2") {
    // 显示第二张图片
    displayImage(3);
    Serial.println("Displaying image 2");
  } else if (data == "3") {
    // 显示第三张图片
    displayImage(2);
    Serial.println("Displaying image 3");
  } else if (data == "4"){
    displayImage(0)
  } else {
    // 显示默认信息
    tft.fillScreen(ST77XX_BLACK);
    tft.setTextColor(ST77XX_WHITE);
    tft.setTextSize(2);
    tft.setCursor(10, 50);
    tft.println("Unknown!");
    Serial.println("Unknown command received");
  }
}

// 显示图片的函数
void displayImage(int rot,const uint16_t *imageData=forward) {
  tft.setRotation(rot)
  // 绘制图片数据
  tft.drawRGBBitmap(0, 0, (const uint16_t*)imageData, TFT_WIDTH, TFT_HEIGHT);  // 从(0,0)位置开始显示图像
}
void loop()
{
  // 接收蓝牙数据
  if (SerialBT.available()) {
    receivedData = SerialBT.readString();  // 去除多余空白符
    Serial.println("Received data: " + receivedData);

    // 根据接收到的数据更新显示屏
    updateDisplay(receivedData);

    if(receivedData == "1"){
      forward_moving();
      stop();
    } else if (receivedData == "2"){
      backward_moving();
      stop();
    } else if (receivedData == "3"){
      leftward_moving();
      stop();
    } else if( receivedData == "4"){
      rightward_moving();
      stop();
    }
  
  }

  delay(100);
}