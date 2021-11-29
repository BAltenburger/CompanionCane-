#define USE_ARDUINO_INTERRUPTS false
#include <PulseSensorPlayground.h>
#include "BluetoothSerial.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include "HX711.h"
#define calibration_factor //will do later
#define DOUT 3
#define CLK 2
#if !defined(CONFIG_BT_ENABLED) || ! defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run 'make menuconfig' to and enable it
#endif
BluetoothSerial SerialBT;
Adafruit_ADXL345_Unified a1(0x68);
Adafruit_ADXL345_Unified a2(0x69);
HX711 lc;
const int pin = A0;
const int th = 550;
byte samplesUntilReport;
const byte SAMPLES_PER_SERIAL_SAMPLE = 10;
PulseSensorPlayground pS;
unsigned long cm;
unsigned long sm;  
void setup(){
  Serial.begin(115200);
  SerialBT.begin("ESP32test");
  
  pS.analogInput(pin);
  pS.setSerial(Serial);
  pS.setThreshold(th);
  pS.setOutputType(SERIAL_PLOTTER);
  samplesUntilReport = SAMPLES_PER_SERIAL_SAMPLE;
  pS.begin();
  a1.begin();
  a2.begin();
  a1.setRange(ADXL345_RANGE_4_G);
  a2.setRange(ADXL345_RANGE_4_G);
  lc.begin(DOUT, CLK);
  lc.set_scale(calibration_factor);
  sm = millis();
}
void loop(){
  cm = millis();
  sensors_event_t event;
  int bpm = pS.getBeatsPerMinute();
  if(Serial.available()){
    SerialBT.write(Serial.read());
  }
  if(SerialBT.available()){
    Serial.write(SerialBT.read());
  }
  if(pS.sawNewSample()){
    if(--samplesUntilReport == (byte) 0){
      samplesUntilReport = SAMPLES_PER_SERIAL_SAMPLE;
      pS.outputSample();
      if(pS.sawStartOfBeat()){
        pS.outputBeat();
      }
    }
    if(cm - sm>= 200){
      a1.getEvent(&event);
      SerialBT.print(bpm);
      SerialBT.print(", ");
      SerialBT.print(event.acceleration.x);
      SerialBT.print(", ");
      SerialBT.print(event.acceleration.y);
      SerialBT.print(", ");
      SerialBT.print(event.acceleration.z);
      a2.getEvent(&event);
      SerialBT.print(", ");
      SerialBT.print(event.acceleration.x);
      SerialBT.print(", ");
      SerialBT.print(event.acceleration.y);
      SerialBT.print(", ");
      SerialBT.print(event.acceleration.z);
      SerialBT.print(", ");
      SerialBT.println(lc.get_units(), 1);
      sm = millis();
    }
  }
}
