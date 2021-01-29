#include <Wire.h>
#include "Adafruit_TCS34725.h"

/* Example code for the Adafruit TCS34725 breakout library */

/* Connect SCL    to analog 5
   Connect SDA    to analog 4
   Connect VDD    to 3.3V DC
   Connect GROUND to common ground */

/* Initialise with default values (int time = 2.4ms, gain = 1x) */
// Adafruit_TCS34725 tcs = Adafruit_TCS34725();

/* Initialise with specific int time and gain values */
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_700MS, TCS34725_GAIN_1X);

void setup(void) {
  Serial.begin(9600);

  if (tcs.begin()) {
    Serial.println("Found sensor");
  } else {
    Serial.println("No TCS34725 found ... check your connections");
    while (1);
  }

  // Now we're ready to get readings!
}

void loop(void) {


//want to normalize the colors it sees
  
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
Serial.print("RED ");
Serial.print(r);
Serial.print(" ");

Serial.print("GREEN ");
Serial.print(g);
Serial.print(" ");

Serial.print("BLUE "); 
Serial.print(b);
Serial.print(" ");

Serial.print("MEAN"); 
Serial.print(" ");
Serial.print(mean); 
Serial.println(" ");
  if(r > mean + sd){
    Serial.println("SEE RED");
    found = 1;
  }
  if(g > mean + sd){
    Serial.println("SEE GREEN");
    found = 1;
  }
  if(b > mean + sd){
    Serial.println("SEE BLUE");
    found = 1;
  }

if(found = 0){
   Serial.println("none");
}

found = 0;


  
}
