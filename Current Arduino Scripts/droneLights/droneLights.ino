
#include <ArduinoBLE.h>
#include <PDM.h>

#include <Arduino_LSM9DS1.h>

// This device's MAC:
// C8:5C:A2:2B:61:86
//#define LEDR        (23u)
//#define LEDG        (22u)
//#define LEDB        (24u)

// Device name
const char* nameOfPeripheral = "Drone_1";
const char* uuidOfService = "00001101-0000-1000-8000-00805f9b34fb";
const char* uuidOfRxChar = "00001142-0000-1000-8000-00805f9b34fb";
const char* uuidOfTxChar = "00001143-0000-1000-8000-00805f9b34fb";


int LED = 2;

//enum for communication stages
//takeoff needs to be handled differntly because the power will shut off the drone
enum currentStage {
  startup,
  acceptedQueue,
  allowedLanding,
  landed,
  takeoff
} CURRENTSTAGE = startup;

bool CONNECTEDPI = false;
int sentMessage = 0;

// BLE Service
BLEService microphoneService(uuidOfService);

// Setup the incoming data characteristic (RX).
const int WRITE_BUFFER_SIZE = 256;
bool WRITE_BUFFER_FIZED_LENGTH = false;

// RX / TX Characteristics
BLECharacteristic rxChar(uuidOfRxChar, BLEWriteWithoutResponse | BLEWrite, WRITE_BUFFER_SIZE, WRITE_BUFFER_FIZED_LENGTH);
BLEByteCharacteristic txChar(uuidOfTxChar, BLERead | BLENotify | BLEBroadcast);

// Buffer to read samples into, each sample is 16-bits
short sampleBuffer[256];

// Number of samples read
volatile int samplesRead;

/*
 *  MAIN
 */
void setup() {

  // Start serial.
  Serial.begin(9600);

  // Ensure serial port is ready.
  //while (!Serial);

   if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
   }


  // Prepare LED pins.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);

  // Configure the data receive callback
  PDM.onReceive(onPDMdata);

  // Start PDM
  startPDM();

  // Start BLE.
  startBLE();

  // Create BLE service and characteristics.
  BLE.setLocalName(nameOfPeripheral);
  BLE.setAdvertisedService(microphoneService);
  microphoneService.addCharacteristic(rxChar);
  microphoneService.addCharacteristic(txChar);
  BLE.addService(microphoneService);

  // Bluetooth LE connection handlers.
  BLE.setEventHandler(BLEConnected, onBLEConnected);
  BLE.setEventHandler(BLEDisconnected, onBLEDisconnected);
  
  // Event driven reads.
  rxChar.setEventHandler(BLEWritten, onRxCharValueUpdate);
  
  // Let's tell devices about us.
  BLE.advertise();
  
  // Print out full UUID and MAC address.
  Serial.println("Peripheral advertising info: ");
  Serial.print("Name: ");
  Serial.println(nameOfPeripheral);
  Serial.print("MAC: ");
  Serial.println(BLE.address());
  Serial.print("Service UUID: ");
  Serial.println(microphoneService.uuid());
  Serial.print("rxCharacteristic UUID: ");
  Serial.println(uuidOfRxChar);
  Serial.print("txCharacteristics UUID: ");
  Serial.println(uuidOfTxChar);
  

  Serial.println("Bluetooth device active, waiting for connections...");
}


//protocall for the drone communication
//1. JOIN_QUEUE_DRONE#_DOCK#

//JOIN_QUEUE_DRONE#_DOCK#
//ACCEPTED_QUEUE_DRONE#_DOCK#
//LAND_DRONE#_DOCK#
//LANDED_DRONE#_DOCK#
//TAKEOFF_DRONE#_DOCK#

void loop()
{
  BLEDevice central = BLE.central();
  
  if (central)
  {

    String Message;
    // Only send data if we are connected to a central device.
    while (central.connected()) {
      connectedLight();

      if(CONNECTEDPI){
       switch (CURRENTSTAGE){
          case startup:

            if(sentMessage == 0){
              Serial.println("sending");
              txChar.writeValue(0);
            }
            break;
          case acceptedQueue:
            break;
          case allowedLanding:
           /// Message = "LANDED_DRONE";
               delay(1000);
                float prevX;
                float prevY;
                float prevZ;
                int currentAddition;
                bool notLanded;
                notLanded = true;
                while(notLanded){
                float x, y, z;
               
               
      
                    if (IMU.accelerationAvailable()) {
                      IMU.readAcceleration(x, y, z);
                     
                 
                      Serial.println(" ");
                     static unsigned long startTime = millis();

                       currentAddition = 0;
                       float bound = 0.1;
                      if(x > prevX - bound && x < prevX + bound){
                           Serial.println("X is stable");
                      }
                      else
                      {
                        currentAddition += 1;
                      }
                      if(y > prevY - bound && y < prevY + bound){
                           Serial.println("Y is stable");
                      }
                      else
                      {
                        currentAddition += 1;
                      }
                       if(z > prevZ - bound && z < prevZ + bound){
                           Serial.println("Z is stable");
                      }
                      else
                      {
                        currentAddition += 1;
                      }
                      prevX = x;
                      prevY = y;
                      prevZ = z;
                      
                      Serial.println(currentAddition);
                      if (currentAddition >= 1){
                          startTime = millis();
                      }
                      if (millis() - startTime >= 1000)
                      {
                     notLanded = false;
                     digitalWrite(LED, HIGH);
                     txChar.writeValue(1); 
                     CURRENTSTAGE = landed;
                     Serial.println("drone is now in landed stage");
                     return;
                      }
                    
                     }
      
                    }
               
                
            //once landing occurs we confim landed on platform before going to landed stage
            
            break;
          case landed:
            break;
          case takeoff:
            break;
       
       }}
       sentMessage = sentMessage + 1;
       if(sentMessage >1000000){
        sentMessage = 0;
       }
       else{
     
       }
       
       }
        
     
    }
  else {
    disconnectedLight();
  }
}


/*
 *  BLUETOOTH
 */
void startBLE() {
  if (!BLE.begin())
  {
    Serial.println("starting BLE failed!");
    while (1);
  }
}


void onRxCharValueUpdate(BLEDevice central, BLECharacteristic characteristic) {
  // central wrote new value to characteristic, update LED
  Serial.print("Characteristic event, read: ");
  byte test[256];
  int dataLength = rxChar.readValue(test, 256);

  String messageRecieved = "";
  for(int i = 0; i < dataLength; i++) {
    messageRecieved += (char)test[i];
  }

  
  Serial.println(messageRecieved);
    if(messageRecieved.equals("ACCEPTED_QUEUE")){
     CURRENTSTAGE = acceptedQueue;
     Serial.println("accepted in queue waiting to land");
  }
  if(messageRecieved.equals("LAND_DRONE")){
     CURRENTSTAGE = allowedLanding;
     Serial.println("allowed to land drone");
  }
  if(messageRecieved.equals("TAKEOFF_DRONE")){
     CURRENTSTAGE = takeoff;
     Serial.println("cleared for takeoff");
  }
   if(messageRecieved.equals("CONNECTED")){
     CURRENTSTAGE = startup;
     CONNECTEDPI = true;
     Serial.println("connected");
  }
  if(messageRecieved.equals("ALIGNED_DRONE")){
     digitalWrite(LED, LOW);
     Serial.println("Drone is aligned turning off light");
  }



  
  Serial.println();
  Serial.print("Value length = ");
  Serial.println(rxChar.valueLength());
}

void onBLEConnected(BLEDevice central) {
  Serial.print("Connected event, central: ");
  Serial.println(central.address());
  connectedLight();
}

void onBLEDisconnected(BLEDevice central) {
  Serial.print("Disconnected event, central: ");
  Serial.println(central.address());
  disconnectedLight();
}


/*
 *  MICROPHONE
 */
void startPDM() {
  // initialize PDM with:
  // - one channel (mono mode)
  // - a 16 kHz sample rate
  if (!PDM.begin(1, 16000)) {
    Serial.println("Failed to start PDM!");
    while (1);
  }
}


void onPDMdata() {
  // query the number of bytes available
  int bytesAvailable = PDM.available();

  // read into the sample buffer
  PDM.read(sampleBuffer, bytesAvailable);

  // 16-bit, 2 bytes per sample
  samplesRead = bytesAvailable / 2;
}


/*
 * LEDS
 */
void connectedLight() {
  digitalWrite(LEDR, LOW);
  digitalWrite(LEDG, HIGH);
}


void disconnectedLight() {
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, LOW);
}
