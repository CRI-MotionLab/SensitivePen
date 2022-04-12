#include "WiFi.h"
#include <OSCMessage.h>

// WIFI CONFIGURATION
WiFiUDP Udp; // A UDP instance to let us send and receive packets over UDP
// const IPAddress outIp(192,168,43,157); // hssnadr
const IPAddress outIp(192,168,1,10); // LANCRY
// Network settings
char ssid[] = "Livebox-FC82"; // your network SSID (name)
char pass[] = "LANCRY666";  // your network password
unsigned int localPort = 7777; // local port to listen for OSC packets
bool _sendOsc = true;

// SENSOR CONFIGURATION
int sensorPin = 38;    // select the input pin for the potentiometer
int ledPin = 13;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor

#define N 100
int dataCollect[N];
int curIndex = 0;
float curMean = 0.0f;
float oldMean = 0.0f;

#define WINDOW 1000
int indxWindw = 0;
float minWindw = 1024;
float maxWindw = 0;
float curMinWindow = 0;
float curMaxWindow = 1024;
float curMeanWindow = 512;
float oldRangeWindow = 512;

long timePrint0 = 0;
int dlyPrint = 10;

boolean isPress = false;


//--------------------------------------
float last_filtered_value = 0.0f;

// SlidingWindowFilter slidWindFilt = SlidingWindowFilter(10, 10);
//--------------------------------------

void setup() {
  Serial.begin(115200);

  // WIFI connection
  if(_sendOsc) {
    Serial.println("Wait for WiFi... ");
    WiFi.begin(ssid, pass);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
    }
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    Udp.begin(localPort);
  }

  
  pinMode(ledPin, OUTPUT);

  // init data collection
  for (int i = 0; i < N; i++) {
    dataCollect[i] = 0;
  }
}

void sendOSC(float val_) {
  if(_sendOsc) {
    // Create message
    OSCMessage msg("/pressure");
    msg.add( val_);
  
    // Send message
    Udp.beginPacket(outIp, 7777);
    msg.send(Udp); // Send the bytes to the SLIP stream
    Udp.endPacket();  // Mark the end of the OSC Packet
    msg.empty();   // Free space occupied by message
    delay(10);
  }
} 

void loop() {
  // update index
  if (curIndex < N && curIndex >= 0) {
    curIndex++;
  }
  else {
    curIndex = 0;
  }

  // update data collection
  dataCollect[curIndex] = analogRead(sensorPin);

  // get moving mean
  oldMean = curMean;
  curMean = 0.0f;
  for (int i = 0; i < N; i++) {
    curMean += dataCollect[i];
  }
  curMean /= N;

  // update window
  if (indxWindw < WINDOW) {
    indxWindw++;
    if (curMean < minWindw) {
      minWindw = curMean;
    }
    if (curMean > maxWindw) {
      maxWindw = curMean;
      curMaxWindow = maxWindw; // TEST CUSTOM
      curMeanWindow = (curMinWindow + curMaxWindow) / 2.0; // TEST CUSTOM
    }
  }
  else {
    // update new thresholds
    curMinWindow = minWindw;
    curMaxWindow = maxWindw;
    curMeanWindow = (curMinWindow + curMaxWindow) / 2.0;

    // reset
    indxWindw = 0;
    minWindw = 1024;
    maxWindw = 0;
  }

  // TEST THRESHOLDS
  if (!isPress) {
    if (oldMean <= curMaxWindow && curMean >= curMaxWindow) {
      isPress = true;
    }
  } else {
    if (oldMean >= curMeanWindow && curMean <= curMeanWindow) {
      isPress = false;
    }
  }
  
  if(millis() - timePrint0 > dlyPrint) {
    // Serial.print(dataCollect[curIndex]);
    // Serial.print('\t');
    Serial.print(curMean);
    sendOSC(curMean);
    /* Serial.print('\t');
    Serial.print(curMinWindow);
    Serial.print('\t');
    Serial.print(curMaxWindow);
    Serial.print('\t');
    Serial.print(curMeanWindow);
    Serial.print('\t');*/
    /* if(isPress) {
      Serial.print(3000);
    } else {
      Serial.print(3600);
    }*/
    Serial.println("");
    // analogWrite(ledPin, curMean);
    timePrint0 = millis();
  }
}
