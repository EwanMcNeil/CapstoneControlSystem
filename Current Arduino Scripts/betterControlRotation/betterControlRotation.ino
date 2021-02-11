#include "PinNames.h"
#include <Wire.h>
#include "Adafruit_TCS34725.h"
#include <Arduino_APDS9960.h>
const unsigned int DELAY = 1000/6;
const byte numChars = 32;
char receivedChars[numChars];
boolean newData = false;
boolean rotate = false;
int currentLED = 0;

uint16_t maxVal = 0;
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_700MS, TCS34725_GAIN_1X);
#include <Servo.h> 

Servo myservo;




int pos = 0; 

void setup() {
    Serial.begin(9600);
    while (!Serial);
      if (tcs.begin()) {
    Serial.println("Found sensor");
  } else {
    Serial.println("No TCS34725 found ... check your connections");
    while (1);
  }

    myservo.attach(9);
    


    Serial.println("<Arduino is ready>");

    pinMode(LED_RED, OUTPUT);

    pinMode(LED_GREEN, OUTPUT);

    pinMode(LED_BLUE, OUTPUT);

    digitalWrite(LED_RED, HIGH);

    digitalWrite(LED_GREEN, HIGH);

    digitalWrite(LED_BLUE, HIGH);


  

  if (!APDS.begin()) {
    Serial.println("Error initializing APDS9960 sensor!");
  }

}

void loop() {
    recvWithStartEndMarkers();
    processNewData();
    acutate();
    checkAlignment();
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void processNewData() {
    if (newData == true) {
        newData = false;
    

    if(strcmp(receivedChars, "ALIGNMENT_START") == 0){
      rotate = true;
 
      currentLED = 1;
    }

    if(strcmp(receivedChars, "QR_ALIGNED") == 0){
      rotate = false;
    }
 
    }
    
}


//Acutate is called when it is time to turn the motor 
//currently simulating the LED blinking
void acutate(){
  if(rotate ==true){
  
  Serial.println("rotate");

  myservo.writeMicroseconds(1600);
  delay(500);
  myservo.writeMicroseconds(1500);
        
  }
  else{
   
     myservo.writeMicroseconds(1500);
  }
}




void foundDrone(){

  

  Serial.println("FOUNDDRONE");
  myservo.writeMicroseconds(1500);

  while(true){
    
  }
  
//   uint16_t r, g, b, c;
// 
//   
//while(true){
//
//    tcs.getRawData(&r, &g, &b, &c);
//    
//    Serial.print("Blue");
//    Serial.print(b);
//    Serial.println(" ");
//    Serial.print("MAX");
//    Serial.print(maxVal);
//    Serial.println(" ");
//
//
//    // maybe check its in range? 
//    
//    if(b > maxVal){
//   
//      //delay(500);
//      maxVal = b;
//      Serial.println("newmax");
//    }
//    if(b < maxVal){
//      myservo.writeMicroseconds(1560);
//      //delay(500);
////      myservo.writeMicroseconds(1500);
////      rotate = false;
////      Serial.println("max value passed");
//      //return;
//      
//    }
//  
//
//
//    
////    
////    if(prevB > b){
////      myservo.writeMicroseconds(1505);
////      delay(1000);
////    }
////    if(prevB < b){
////        
////        myservo.writeMicroseconds(1495);
////        delay(1000);
////    }
////
////    prevB = b;
////    Serial.println("PREVB");
////    Serial.println(prevB);
//  
}
  




void checkAlignment(){

  uint16_t r, g, b, c, colorTemp, lux;
  double mean, sumofDif, varience,sd;

  tcs.getRawData(&r, &g, &b, &c);
  // colorTemp = tcs.calculateColorTemperature(r, g, b);
  colorTemp = tcs.calculateColorTemperature_dn40(r, g, b, c);
  lux = tcs.calculateLux(r, g, b);

  mean = (r + g + b)/3;
  sumofDif = sq(r-mean) + sq(g-mean) + sq(b-mean);
  varience = sumofDif/3;
  sd = sqrt(varience);

  int found = 0;


    if(r > mean + sd){
     
      found = 1;
    }
    if(g > mean + sd){
      
      found = 1;
    }
    if(b > mean + sd){

     
     //enter the found drone mode
     foundDrone();
      
      found = 1;
    }

  if(found = 0){
    Serial.println("none");
  }

  found = 0;

}
