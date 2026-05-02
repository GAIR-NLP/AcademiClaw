

#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library for ST7789
#include <SPI.h>

#include <Arduino.h>
#include <driver/I2S.h>
#include "es8311.h"

#include <WiFi.h>
#include <HTTPClient.h>
#include "AudioFileSourceHTTPStream.h"
#include "AudioGeneratorMP3.h"
#include "AudioOutputI2S.h"

// Wi-Fi 设置
const char* ssid = "TP-LINK_2803";
const char* password = "54010990";

// MP3 文件 URL
//const char* mp3URL = "http://192.168.71.222/011.mp3";
char mp3URL[] = "http://101.35.153.214:8888/12.mp3";

//char* mp3URL = "http://123.60.16.94/live/1270/64k.mp3";
// 创建音频对象
AudioGeneratorMP3* mp3;
AudioFileSourceHTTPStream* file;
AudioOutputI2S* out;
//#define ESP32
// I2C
#define SDAPIN 32        // I2C Data,  Adafruit ESP32 S3 3, Sparkfun Thing Plus C 23
#define SCLPIN 33       // I2C Clock, Adafruit ESP32 S3 4, Sparkfun Thing Plus C 22
#define I2CSPEED 60000  // Clock Rate
#define ES8388ADDR 0x18 // Address of ES8388 I2C port

// I2S, your configuration for the ES8388 board
#define MCLKPIN 27 // Master Clock
#define BCLKPIN 14  // Bit Clock
#define WSPIN 26  // Word select
#define DOPIN 12   // This is connected to DI on ES8388 (MISO)
#define DIPIN  13   // This is connected to DO on ES8388 (MOSI)



#define TFT_CS 5
// #define TFT_RST        15
#define TFT_DC 21
#define TFT_MOSI 23 // Data out
#define TFT_SCLK 18 // Clock out

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, 0);

float p = 3.1415926;


void testlines(uint16_t color)
{
  tft.fillScreen(ST77XX_BLACK);
  for (int16_t x = 0; x < tft.width(); x += 6)
  {
    tft.drawLine(0, 0, x, tft.height() - 1, color);
    delay(0);
  }
  for (int16_t y = 0; y < tft.height(); y += 6)
  {
    tft.drawLine(0, 0, tft.width() - 1, y, color);
    delay(0);
  }

  tft.fillScreen(ST77XX_BLACK);
  for (int16_t x = 0; x < tft.width(); x += 6)
  {
    tft.drawLine(tft.width() - 1, 0, x, tft.height() - 1, color);
    delay(0);
  }
  for (int16_t y = 0; y < tft.height(); y += 6)
  {
    tft.drawLine(tft.width() - 1, 0, 0, y, color);
    delay(0);
  }

  tft.fillScreen(ST77XX_BLACK);
  for (int16_t x = 0; x < tft.width(); x += 6)
  {
    tft.drawLine(0, tft.height() - 1, x, 0, color);
    delay(0);
  }
  for (int16_t y = 0; y < tft.height(); y += 6)
  {
    tft.drawLine(0, tft.height() - 1, tft.width() - 1, y, color);
    delay(0);
  }

  tft.fillScreen(ST77XX_BLACK);
  for (int16_t x = 0; x < tft.width(); x += 6)
  {
    tft.drawLine(tft.width() - 1, tft.height() - 1, x, 0, color);
    delay(0);
  }
  for (int16_t y = 0; y < tft.height(); y += 6)
  {
    tft.drawLine(tft.width() - 1, tft.height() - 1, 0, y, color);
    delay(0);
  }
}

void testdrawtext(char* text, uint16_t color)
{
  tft.fillScreen(ST77XX_BLACK);
  tft.setCursor(20, 20);
  tft.setTextColor(color);
  tft.setTextWrap(true);
  tft.print(text);
}

void testfastlines(uint16_t color1, uint16_t color2)
{
  tft.fillScreen(ST77XX_BLACK);
  for (int16_t y = 0; y < tft.height(); y += 5)
  {
    tft.drawFastHLine(0, y, tft.width(), color1);
  }
  for (int16_t x = 0; x < tft.width(); x += 5)
  {
    tft.drawFastVLine(x, 0, tft.height(), color2);
  }
}

void testdrawrects(uint16_t color)
{
  tft.fillScreen(ST77XX_BLACK);
  for (int16_t x = 0; x < tft.width(); x += 6)
  {
    tft.drawRect(tft.width() / 2 - x / 2, tft.height() / 2 - x / 2, x, x, color);
  }
}

void testfillrects(uint16_t color1, uint16_t color2)
{
  tft.fillScreen(ST77XX_BLACK);
  for (int16_t x = tft.width() - 1; x > 6; x -= 6)
  {
    tft.fillRect(tft.width() / 2 - x / 2, tft.height() / 2 - x / 2, x, x, color1);
    tft.drawRect(tft.width() / 2 - x / 2, tft.height() / 2 - x / 2, x, x, color2);
  }
}

void testfillcircles(uint8_t radius, uint16_t color)
{
  for (int16_t x = radius; x < tft.width(); x += radius * 2)
  {
    for (int16_t y = radius; y < tft.height(); y += radius * 2)
    {
      tft.fillCircle(x, y, radius, color);
    }
  }
}

void testdrawcircles(uint8_t radius, uint16_t color)
{
  for (int16_t x = 0; x < tft.width() + radius; x += radius * 2)
  {
    for (int16_t y = 0; y < tft.height() + radius; y += radius * 2)
    {
      tft.drawCircle(x, y, radius, color);
    }
  }
}

void testtriangles()
{
  tft.fillScreen(ST77XX_BLACK);
  uint16_t color = 0xF800;
  int t;
  int w = tft.width() / 2;
  int x = tft.height() - 1;
  int y = 0;
  int z = tft.width();
  for (t = 0; t <= 15; t++)
  {
    tft.drawTriangle(w, y, y, x, z, x, color);
    x -= 4;
    y += 4;
    z -= 4;
    color += 100;
  }
}

void testroundrects()
{
  tft.fillScreen(ST77XX_BLACK);
  uint16_t color = 100;
  int i;
  int t;
  for (t = 0; t <= 4; t += 1)
  {
    int x = 0;
    int y = 0;
    int w = tft.width() - 2;
    int h = tft.height() - 2;
    for (i = 0; i <= 16; i += 1)
    {
      tft.drawRoundRect(x, y, w, h, 5, color);
      x += 2;
      y += 3;
      w -= 4;
      h -= 6;
      color += 1100;
    }
    color += 100;
  }
}

void tftPrintTest()
{
  tft.setTextWrap(false);
  tft.fillScreen(ST77XX_BLACK);
  tft.setCursor(0, 30);
  tft.setTextColor(ST77XX_RED);
  tft.setTextSize(1);
  tft.println("Hello World!");
  tft.setTextColor(ST77XX_YELLOW);
  tft.setTextSize(2);
  tft.println("Hello World!");
  tft.setTextColor(ST77XX_GREEN);
  tft.setTextSize(3);
  tft.println("Hello World!");
  tft.setTextColor(ST77XX_BLUE);
  tft.setTextSize(4);
  tft.print(1234.567);
  delay(1500);
  tft.setCursor(0, 0);
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextColor(ST77XX_WHITE);
  tft.setTextSize(0);
  tft.println("Hello World!");
  tft.setTextSize(1);
  tft.setTextColor(ST77XX_GREEN);
  tft.print(p, 6);
  tft.println(" Want pi?");
  tft.println(" ");
  tft.print(8675309, HEX); // print 8,675,309 out in HEX!
  tft.println(" Print HEX!");
  tft.println(" ");
  tft.setTextColor(ST77XX_WHITE);
  tft.println("Sketch has been");
  tft.println("running for: ");
  tft.setTextColor(ST77XX_MAGENTA);
  tft.print(millis() / 1000);
  tft.setTextColor(ST77XX_WHITE);
  tft.print(" seconds.");
}

void mediabuttons()
{
  // play
  tft.fillScreen(ST77XX_BLACK);
  tft.fillRoundRect(25, 10, 78, 60, 8, ST77XX_WHITE);
  tft.fillTriangle(42, 20, 42, 60, 90, 40, ST77XX_RED);
  delay(500);
  // pause
  tft.fillRoundRect(25, 90, 78, 60, 8, ST77XX_WHITE);
  tft.fillRoundRect(39, 98, 20, 45, 5, ST77XX_GREEN);
  tft.fillRoundRect(69, 98, 20, 45, 5, ST77XX_GREEN);
  delay(500);
  // play color
  tft.fillTriangle(42, 20, 42, 60, 90, 40, ST77XX_BLUE);
  delay(50);
  // pause color
  tft.fillRoundRect(39, 98, 20, 45, 5, ST77XX_RED);
  tft.fillRoundRect(69, 98, 20, 45, 5, ST77XX_RED);
  // play color
  tft.fillTriangle(42, 20, 42, 60, 90, 40, ST77XX_GREEN);
}

// // I2C
// #define SDAPIN 0        // I2C Data,  Adafruit ESP32 S3 3, Sparkfun Thing Plus C 23
// #define SCLPIN 1        // I2C Clock, Adafruit ESP32 S3 4, Sparkfun Thing Plus C 22
// #define I2CSPEED 60000  // Clock Rate
// #define ES8388ADDR 0x18 // Address of ES8388 I2C port

// // I2S, your configuration for the ES8388 board
// #define MCLKPIN 10 // Master Clock
// #define BCLKPIN 8  // Bit Clock
// #define WSPIN 12   // Word select
// #define DOPIN 11   // This is connected to DI on ES8388 (MISO)
// #define DIPIN 7    // This is connected to DO on ES8388 (MOSI)
// 定义INMP441管脚
#define I2S_WS 26
#define I2S_SD 12
#define I2S_SCK 14
// I2S端口号
#define I2S_PORT I2S_NUM_0

// I2S读取到数据的缓存区
#define bufferLen 2400
int16_t sBuffer[bufferLen];

#define EXAMPLE_RECV_BUF_SIZE (2048)
#define EXAMPLE_SAMPLE_RATE (16000)
#define EXAMPLE_MCLK_MULTIPLE I2S_MCLK_MULTIPLE_256
#define EXAMPLE_VOICE_VOLUME CONFIG_EXAMPLE_VOICE_VOLUME
#if CONFIG_EXAMPLE_MODE_ECHO
#define EXAMPLE_MIC_GAIN CONFIG_EXAMPLE_MIC_GAIN
#endif

void i2s_install()
{
  // 按照以下配置来启动I2S端口

//   const i2s_config_t i2s_config = {
//       .mode = static_cast<i2s_mode_t>(I2S_MODE_MASTER | I2S_MODE_TX | I2S_MODE_RX),
//       .sample_rate = 44100,
//       .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
//       .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,
// #if ESP_IDF_VERSION_MAJOR > 3
//       .communication_format = I2S_COMM_FORMAT_STAND_I2S, // static_cast<i2s_comm_format_t>(I2S_COMM_FORMAT_STAND_I2S|I2S_COMM_FORMAT_STAND_MSB),
// #else
//       .communication_format = static_cast<i2s_comm_format_t>(I2S_COMM_FORMAT_I2S | I2S_COMM_FORMAT_I2S_MSB),
// #endif
//       // .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1, // default interrupt priority
//       // .dma_buf_count = 3,
//       // .dma_buf_len = 600,
//       // .use_apll = false,
//       // .tx_desc_auto_clear = true
//       .intr_alloc_flags = ESP_INTR_FLAG_LEVEL2 | ESP_INTR_FLAG_IRAM,
//       .dma_buf_count = 3,
//       .dma_buf_len = 300,
//       .use_apll = true,
//       .tx_desc_auto_clear = true,
//      };
  i2s_config_t i2s_cfg = {
      .mode = static_cast<i2s_mode_t>(I2S_MODE_MASTER | I2S_MODE_TX | I2S_MODE_RX),
      .sample_rate = EXAMPLE_SAMPLE_RATE,
      .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
      .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,
      .communication_format = I2S_COMM_FORMAT_STAND_I2S,
      .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
      .dma_buf_count = 8,
      .dma_buf_len = 64,
      .use_apll = false,
      .tx_desc_auto_clear = true,
      .fixed_mclk = 0,
      .mclk_multiple = EXAMPLE_MCLK_MULTIPLE,
      .bits_per_chan = I2S_BITS_PER_CHAN_16BIT,
#if SOC_I2S_SUPPORTS_TDM
      .chan_mask = static_cast<i2s_channel_t>(I2S_TDM_ACTIVE_CH0 | I2S_TDM_ACTIVE_CH1),
      .total_chan = 2,
      .left_align = false,
      .big_edin = false,
      .bit_order_msb = false,
      .skip_msk = false,
#endif

  };
  // i2s pinout
  static const i2s_pin_config_t pin_config = {
      .mck_io_num = I2S_MCLK, //0
      .bck_io_num = I2S_SCK, // 14
      .ws_io_num = I2S_WS,   // 26
      .data_out_num = I2S_DOUT,  // 12
      .data_in_num = I2S_DIN // 13 I2S_PIN_NO_CHANGE
  };

  // now configure i2s with constructed pinout and config
  i2s_driver_install(I2S_NUM_0, &i2s_cfg, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pin_config);

}

int SWITCH_PIN = 34;
int switchVal = 1;
void setupmp3(void)
{

  Serial.begin(115200);
  Serial.print(F("Hello! ST77xx TFT Test"));
  pinMode(25, OUTPUT);
  digitalWrite(25, HIGH);

  pinMode(19, OUTPUT);
  // digitalWrite(19, LOW);
  analogWrite(19, 150);
  Wire.begin(I2C_SDA, I2C_SCL, I2C_FREQ);
  // Audio_codeC(ES8311);
   //music.begin();
   //music.I2S(I2S_BCK, I2S_DOUT, I2S_WS);
  es8311_init(AUDIO_HAL_SAMPLE_RATE);
  Serial.print(F("i2s install 1\n"));
  es8311_set_voice_volume(45);
  Serial.print(F("i2s install 2\n"));
  es8311_set_mic_gain(ES8311_MIC_GAIN_12DB);

  i2s_install();
  Serial.print(F("i2s install \n"));
  Serial.print(F("Set pin ok\n"));
  i2s_start(I2S_PORT);

  Serial.println(F("Initialized"));
  uint16_t time = millis();

  tft.initR(INITR_144GREENTAB);      // Init ST7735S chip, black tab
  tft.fillScreen(ST77XX_BLACK);
  time = millis() - time;

  Serial.println(time, DEC);
  delay(500);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi!");

  // 初始化I2S输出AudioOutputI2S(int port, int output_mode, int dma_buf_count, int use_apll)
  //SetPinout(int bclk, int wclk, int dout)
  out = new AudioOutputI2S(0, 0, 8, 0);
  out->SetPinout(14, 26, 12);
  out->SetRate(EXAMPLE_SAMPLE_RATE);
  out->begin();

  // 从URL获取MP3文件并播放
  file = new AudioFileSourceHTTPStream(mp3URL);
  mp3 = new AudioGeneratorMP3();
  mp3->begin(file, out);
  // large block of text
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextSize(1);
 // testdrawtext("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur adipiscing ante sed nibh tincidunt feugiat. Maecenas enim massa, fringilla sed malesuada et, malesuada sit amet turpis. Sed porttitor neque ut ante pretium vitae malesuada nunc bibendum. Nullam aliquet ultrices massa eu hendrerit. Ut sed nisi lorem. In vestibulum purus a tortor imperdiet posuere. ", ST77XX_WHITE);
  testdrawtext(mp3URL, ST7735_YELLOW);
  delay(1000);
  pinMode(SWITCH_PIN, INPUT);

}

// // digital to analog：麦克风输入为digital code(binary)， 需要将编码转换成相应的电压值才能播放
// void i2s_adc_data_scale(int8_t *d_buff, int16_t *s_buff, uint32_t len)
// {
//   uint32_t j = 0;
//   int16_t dac_value = 0;
//   // 一个采样点是2byte，每2个byte
//   for (int i = 0; i < len; i += 2)
//   {
//     dac_value =s_buff[i + 1] <<8;
//     dac_value +=s_buff[i + 0];
//     dac_value/=16;
//     d_buff[j++] = dac_value&0xff;
//     d_buff[j++] = (dac_value >> 8) & 0xff;
//   }
// }
extern char rawData[];
size_t written_bytes = 0;




void loopmp3()
{
  switchVal = digitalRead(SWITCH_PIN);
  // 播放MP3文件
  // if (mp3->isRunning())
  // {
  //   mp3->loop();
  // }
  // else
  // {
  //   mp3->stop();

  //   Serial.println("Playback stopped");

  //   delay(1000);
  //   Serial.println(mp3URL);
  //   // 初始化I2S输出
  // }


  // if (mp3->isRunning()) { // 是否在播放
  //   if (!mp3->loop()) {    // 是否播放完了
  //     mp3->stop();        // 停止播放
  //     file->close();
  //     delete file;
  //     delete mp3;
  //     mp3 = new AudioGeneratorMP3();
  //   }
  // }
  // else {
  //   if (switchVal == 0) {  // 开关接通为低电平
  //     if (mp3URL[28] <= '7') mp3URL[28]++;
  //     else mp3URL[28] = '1';
  //     Serial.printf(mp3URL);
  //     delay(1000);
  //     file = new AudioFileSourceHTTPStream(mp3URL); // 初始化音频文件
  //     Serial.printf("MP3 done\n");
  //     delay(1000);
  //     mp3->begin(file, out);  // 开始播放文件
  //   }
  // }

  if (switchVal == 0) {  // 开关接通为低电平

    while (switchVal == 0)
    {
      switchVal = digitalRead(SWITCH_PIN);
    }
    if (mp3->isRunning()) { // 是否在播放
      // if (!mp3->loop()) {    // 是否播放完了
      mp3->stop();        // 停止播放
      file->close();
      delete file;
      delete mp3;
      mp3 = new AudioGeneratorMP3();
      //  }
    }
    //else {
    if (mp3URL[28] <= '7') mp3URL[28]++;
    else mp3URL[28] = '1';
    Serial.printf(mp3URL);
    testdrawtext(mp3URL, ST7735_YELLOW);
    file = new AudioFileSourceHTTPStream(mp3URL); // 初始化音频文件
    Serial.printf("MP3 done\n");
    delay(100);
    mp3->begin(file, out);  // 开始播放文件
    // }

  }

  if (mp3->isRunning()) { // 是否在播放
    if (!mp3->loop()) {    // 是否播放完了
      mp3->stop();        // 停止播放
      file->close();
      delete file;
      delete mp3;
      mp3 = new AudioGeneratorMP3();
    }
  }


  // if (written_bytes >= 640000)
  //   written_bytes = 0;
  // size_t bytes_to_write = 640000 - written_bytes;
  // i2s_write(I2S_NUM_0, &rawData[written_bytes], bytes_to_write, &written_bytes, portMAX_DELAY);


 // Serial.write(&rawData[written_bytes], bytes_to_write);
  //int8_t flash_write_buff[4800];
      //   tft.invertDisplay(true);
      //  // copier.copy();
      //   delay(500);
      //   tft.invertDisplay(false);
      //   delay(500);
      // 持续打印两条参考线
  //    int rangelimit = 3000;
  // Serial.print(rangelimit * -1);
  // Serial.print(" ");
  // Serial.print(rangelimit);
  // Serial.print(" ");
  // memset(sBuffer, 0, bufferLen);
  // // 获取I2S读取的数据
  // size_t bytesIn = 0;
  // esp_err_t result = i2s_read(I2S_NUM_0, sBuffer, bufferLen, &bytesIn, 1000);

  // if (result == ESP_OK)
  // {
  //   // 读取缓存区


  //     //Serial.write((char*)sBuffer, (int)bytesIn);
  //    // i2s_adc_data_scale(flash_write_buff, (int16_t *)sBuffer, bytesIn);
  //    for(int i = 0; i< bytesIn/2;i++)
  //      sBuffer[i] /=12;
  //    Serial.write((char *)sBuffer, (int)bytesIn);
  //    esp_err_t result = i2s_write(I2S_NUM_0, sBuffer, bytesIn, &bytesIn, 1000);
  //    // result = i2s_write(I2S_NUM_0, sBuffer, bytesIn, &bytesIn, 1000);
  //    // int16_t muestras = bytesIn / 8;
  //    // if (muestras > 0)
  //    // {
  //    //   float promedio = 0;
  //    //   for (int16_t i = 0; i < muestras; ++i)
  //    //   {
  //    //     promedio += (sBuffer[i]);
  //    //   }
  //    //   promedio /= muestras;
  //    //   // 串口打印出获取到的数据曲线
  //    //   Serial.println(promedio);
  //    // }
  // }
}
