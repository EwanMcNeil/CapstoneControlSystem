#include "PinNames.h"

#include <Arduino_APDS9960.h>
const unsigned int DELAY = 1000/6;
const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

boolean rotate = false;
int currentLED = 0;




void setup() {
    Serial.begin(9600);
    while (!Serial);

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
   
          digitalWrite(LED_GREEN, LOW);
          delay(DELAY);
          digitalWrite(LED_GREEN, HIGH);
          delay(DELAY);
 
        
  }
}


void checkAlignment(){
if (APDS.proximityAvailable()) {

  if(rotate){
    int proximity = APDS.readProximity();
  
    if (proximity < 200){
      rotate = false;
      Serial.print("<ALIGNMENT_FINISHED>\n");
    }
  }
  }
  delay(100);  

}
