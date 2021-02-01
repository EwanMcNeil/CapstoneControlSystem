// https://rootsaid.com/arduino-ble-example/
// Characteristic info.
// https://www.arduino.cc/en/Reference/ArduinoBLEBLECharacteristicBLECharacteristic

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




//enum for communication stages
//takeoff needs to be handled differntly because the power will shut off the drone
enum currentStage {
  startup,
  acceptedQueue,
  allowedLanding,
  landed,
  takeoff
} CURRENTSTAGE = startup;

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
  while (!Serial);

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

       switch (CURRENTSTAGE){
          case startup:
            txChar.writeValue(0);
            delay(5000); 
            break;
          case acceptedQueue:
            break;
          case allowedLanding:
           /// Message = "LANDED_DRONE";
          delay(1000);
          
          while(true){
         float x, y, z;

              if (IMU.accelerationAvailable()) {
                IMU.readAcceleration(x, y, z);
            
                Serial.print(x);
                Serial.print('\t');
                Serial.print(y);
                Serial.print('\t');
                Serial.println(z);
              }
           if(x == 0.0 && y == 0.0 && z == 0.0){
                break;
               }
          }
            //once landing occurs we confim landed on platform before going to landed stage
             txChar.writeValue(1); 
             CURRENTSTAGE = landed;
             Serial.println("drone is now in landed stage");
            break;
          case landed:
            break;
          case takeoff:
            break;
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

  String messageRecieved = String((char *)test);
  Serial.println(messageRecieved);
    if(messageRecieved.equals("ACCEPTED_QUEUE")){
     CURRENTSTAGE = acceptedQueue;
     Serial.println("accepted in queue waiting to land");
  }
  if(messageRecieved.equals("LAND_DRONE")){
     CURRENTSTAGE = acceptedQueue;
     Serial.println("allowed to land drone");
  }
  if(messageRecieved.equals("TAKEOFF_DRONE")){
     CURRENTSTAGE = acceptedQueue;
     Serial.println("cleared for takeoff");
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
