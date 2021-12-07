#define USE_ARDUINO_INTERRUPTS false
#include <PulseSensorPlayground.h>
#include "BluetoothSerial.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include "HX711.h"
#define calibration_factor -10000.0 //number we calibrated 12/6
#define DOUT 4
#define CLK 2 //not 100% sure if this is correct but the sck is connected to pin GPIO2. This is also associated with the blue led on the board and will cause it to flash continuously
#if !defined(CONFIG_BT_ENABLED) || ! defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run 'make menuconfig' to and enable it
#endif
BluetoothSerial SerialBT;    //creates object for serial bluetooth connection
Adafruit_ADXL345_Unified a1  //creates object for the accelerometer. right now planning on only 1 accelerometer
HX711 lc;
const int pin = 34;  //pin defaults to A0 but for wolfgang's circuit it is on the GPIO34
const int th = 550;
byte samplesUntilReport;
const byte SAMPLES_PER_SERIAL_SAMPLE = 10;
PulseSensorPlayground pS; //creates the pulse sensor object, pS
unsigned long cm;    //these two longs are used to track the time passed to read data every 200 ms
unsigned long sm;  
void setup(){
  Serial.begin(115200);   //starts serial with baudrate of 115200. when testing using serial monitor make sure to set the baudrate to this value along with any python code
  SerialBT.begin("ESP32"); //this sets the name of the device and makes it discoverable via bluetooth
  
  pS.analogInput(pin);   //sets pulse sensor input to be from pin 34
  pS.setSerial(Serial);  //sets pulse sensor serial to the serial set before and will later output raw values that can be viewed in the serial monitor
  pS.setThreshold(th);   //sets pulse sensor threshold
  pS.setOutputType(SERIAL_PLOTTER);  //sets output type which basically graphs the raw values from the pulse sensor which can viewed from the serial plotter menu
  samplesUntilReport = SAMPLES_PER_SERIAL_SAMPLE; //sets number of samples before calculating heart rate
  pS.begin();  //starts the pulseSensor
  a1.begin();  //starts the accelerometer
  //a2.begin(); //commented out for now since aryan will figure out how to differentiate data from the 2 accelerometers
  a1.setRange(ADXL345_RANGE_4_G);  //sets the range of the accelerometer
  //a2.setRange(ADXL345_RANGE_4_G); //commented out for now since aryan will figure out how to differentiate data from the 2 accelerometers
  lc.begin(DOUT, CLK);  //starts the load cell
  lc.set_scale(calibration_factor);  //calibrates the load cell based on the calibration factor. I have not calibrated it and am just using a default value that i found online
  lc.tare(); //tares the scale based on the calibration factor
  sm = millis();  //this sets the start time of the code and is later updated to keep track of every interval of 200ms
}
void loop(){
  cm = millis();  //this keeps track of the time in each interval of the loop and is later used and compared with the start time variable "sm" to see if 200ms passed
  sensors_event_t event;  //this is used in tandem with the accelerometer to get the "event" data
  a1.getEvent(&event);
  int bpm = pS.getBeatsPerMinute();  //this gets the bpm calculated from the esp32 and pulse sensor data
  if(Serial.available()){    //this section sets the serial connection up for both the bluetooth and wired connection if there is a wired connection.
    SerialBT.write(Serial.read());
  }
  if(SerialBT.available()){
    Serial.write(SerialBT.read());
  }
  if(pS.sawNewSample()){ //checks if pulse sensor has read a pulse and outputs raw data
    if(--samplesUntilReport == (byte) 0){ 
      samplesUntilReport = SAMPLES_PER_SERIAL_SAMPLE;
      pS.outputSample();
      if(pS.sawStartOfBeat()){
        pS.outputBeat();
      }
    }
    if(cm - sm>= 50){  //checks to see if 200ms passed and prints all the values to the bluetooth serial that is then read by the python code
      SerialBT.print(bpm);
      SerialBT.print(",");
      SerialBT.print(event.acceleration.x);
      SerialBT.print(",");
      SerialBT.print(event.acceleration.y);
      SerialBT.print(",");
      SerialBT.print(event.acceleration.z);
      //a2.getEvent(&event);
      SerialBT.print(",");
      //SerialBT.print(event.acceleration.x);
      //SerialBT.print(", ");
      //SerialBT.print(event.acceleration.y);
      //SerialBT.print(", ");
      //SerialBT.print(event.acceleration.z);
      //SerialBT.print(", ");
      SerialBT.println(lc.get_units(), 1);
      sm = cm;  //updates the starting time to keep track of consecutive 200ms interval
    }
  }
}
