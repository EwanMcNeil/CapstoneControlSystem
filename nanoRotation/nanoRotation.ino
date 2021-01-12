#include "PinNames.h"
#include <Arduino_LSM9DS1.h>
const unsigned int DELAY = 1000/6;



const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

boolean blinking = false;
int currentLED = 0;




void setup() {
    Serial.begin(9600);
    Serial.println("<Arduino is ready>");

    pinMode(LED_RED, OUTPUT);

    pinMode(LED_GREEN, OUTPUT);

    pinMode(LED_BLUE, OUTPUT);

    digitalWrite(LED_RED, HIGH);

    digitalWrite(LED_GREEN, HIGH);

    digitalWrite(LED_BLUE, HIGH);

     if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Acceleration in G's");
  Serial.println("X\tY\tZ");

}

void loop() {
    recvWithStartEndMarkers();
    showNewData();
    blinkLED();
    motionDetection();
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

void showNewData() {
    if (newData == true) {
        newData = false;
    

    if(strcmp(receivedChars, "red") == 0){
      blinking = true;
      currentLED = 1;
 
    }
    
    if(strcmp(receivedChars, "green") == 0){
      blinking = true;
      currentLED = 2;
 
    }
    
    if(strcmp(receivedChars, "blue") == 0){
      blinking = true;
      currentLED = 3;
 
    }
    
    if(strcmp(receivedChars, "stop") == 0){
      blinking = false;
 
    }
 
    }
    
}

void blinkLED(){
  if(blinking ==true){
      switch (currentLED){
        case 1:
          digitalWrite(LED_RED, LOW);
          delay(DELAY);
          digitalWrite(LED_RED, HIGH);
          delay(DELAY);
          break;
        case 2:
          digitalWrite(LED_GREEN, LOW);
          delay(DELAY);
          digitalWrite(LED_GREEN, HIGH);
          delay(DELAY);
          break;
        case 3:
          digitalWrite(LED_BLUE, LOW);
          delay(DELAY);
          digitalWrite(LED_BLUE, HIGH);
          delay(DELAY);
          break;
        
      }


    
  }
}


void motionDetection(){

        
 float x, y, z;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

   if(y < 0){
    if(z <0){
        Serial.print("flip");
    }
   }
  }
}
