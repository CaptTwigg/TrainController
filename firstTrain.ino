// dette program virker, kan resette alle lyssignaler

#include "int.h"

#define DCC_PIN     4                         // DCC out
#define PREAMBLE    0                         // definitions for state machine
#define SEPERATOR   1                         // definitions for state machine
#define SENDBYTE    2                         // definitions for state machine
#define MAXMSG      2

typedef enum STOPPING {
  HARD,
  GLIDE,
  FAST,
};

typedef enum SWITCH {
  TURN,
  STRAIGHT,
};

struct signalAndSwitch {
  int addr;
  int data;
  int data2;
};


int incomingByte = 0;
unsigned char preample1;                      // global variabel for preample part 1
unsigned char preample2;                      // global variabel for preample part 2
unsigned char addr;                           // global variabel adresse
unsigned char data;                           // global variabel kommando
unsigned char checksum;                       // global variabel for checksum
unsigned char inputType;
unsigned char locoAddr  = 9;
unsigned char locoSpeed = 127;
unsigned int  accAddr;
unsigned char accData;
unsigned char  swhifter = 101;
int trigPin  = 9;
int echoPin  = 8;
int trig15 = 6;
int trig12 = 5;
long duration;
int distance = 1000;



void setup()
{
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(DCC_PIN, OUTPUT);      // enable styrepin som output
  pinMode(trig12, INPUT);
  pinMode(trig15, INPUT);
  //pinMode(dirpin,INPUT_PULLUP);// dirpin som input
  SetupTimer2();

  addr      = locoAddr;          // default lokoadresse
  data      = locoSpeed;         // default hastighed og retning, rew speed = 4


  pinMode(LED_BUILTIN, OUTPUT);
  //signalAndSwitchSend(151, 1);
  startTrain(8, "forward", 8);

  int switches[] = {251, 249, 250, 252};
  for (int i = 0; i < 4; i++) {
    //signalAndSwitchSend(switches[i],1);
  }


}

void loop()
{
  manda();
      //signalAndSwitchSend(102, STRAIGHT);

  /*int press12 = digitalRead(trig12);
  int press15 = digitalRead(trig15);
  Serial.print("press12: ");
  Serial.println(press12);
  Serial.print("press15: ");
  Serial.println(press15);
*/
  


  if (Serial.available()) {
    String dataset = Serial.readString();
    Serial.println("python: " + dataset);

    if (dataset.equals("blink")) {
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    }
    if (dataset.equals("noblink")) {
      digitalWrite(LED_BUILTIN, LOW);   // turn the LED on (HIGH is the voltage level)
    }

    if (dataset.startsWith("EStop")) {
      eStop();
      Serial.println("Emergency Stop");
    }

    if (dataset.startsWith("train")) {
      String direct = getValue(dataset, ' ', 1);
      direct.trim();
      String train =  getValue(dataset, ' ', 2);
      train.trim();
      char trainInt = train.toInt();
      String trainSpeed =  getValue(dataset, ' ', 3);
      trainSpeed.trim();
      int trainSpeedInt = (trainSpeed).toInt();

      if (direct.equals("start")) {

        if (trainSpeedInt < 0) {
          startTrain(trainInt, "backwards", trainSpeedInt * -1);
        }
        if (trainSpeedInt > 0) {
          startTrain(trainInt, "forward", trainSpeedInt);
        }

      }
      if (direct.equals("stop")) {
        stopTrain(trainInt, GLIDE);
      }

    }
  }
}

void startTrain(char trainNumber, String locodirection, int locospeed) {
  int direct = 64; // backwards
  if (locodirection.equals("forward")) {
    direct = 96; // forward
  }
  data = direct + locospeed;
  // Serial.print("startTrainData : "); Serial.println(data);
  assemble_dcc_msg(trainNumber, data);
  delay(50);
  data = 0x80;
  assemble_dcc_msg(addr, data);
  delay(50);
}

void stopTrain(char trainNumber, int stop) {
  if (stop == GLIDE) {
    data = 0x60;
  }
  if (stop == HARD) {
    data = 0x61;
  }
  if (stop == FAST) {
    data = 0x40;
  }
  // Serial.print("startTrainData : ");Serial.println(data);
  assemble_dcc_msg(trainNumber, data);
  delay(50);
  data = 0x80;
  assemble_dcc_msg(addr, data);
  delay(50);
}

void eStop() {
  assemble_dcc_msg(0, 1);
  delay(50);
}


String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }

  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void signalAndSwitchSend(int a, int b) {
  struct signalAndSwitch ss;
  int address = (a / 4) + 1;
  int dd = (a % 4) - 1;

  if (dd < 0) {
    address--;
    dd = 3;
  }

  ss.addr  = B10 << 6 ^ address;
  ss.data  = (B11111 << 2 ^ dd) << 1 ^ b;
  ss.data2 = (B11110 << 2 ^ dd) << 1 ^ b;
  assemble_dcc_msg(ss.addr, ss.data); delay(50);
  assemble_dcc_msg(ss.addr, ss.data2); delay(50);

}


void manda() {

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2;
  // Prints the distance on the Serial Monitor


  if (distance < 5) {
    signalAndSwitchSend(102, TURN);
    stopTrain(40, GLIDE);
    startTrain(8, "forward", 8);
    startTrain(8, "forward", 8);
    Serial.print("Distance: ");
    Serial.println(distance);
    delay(1000);
  }
  if (distance > 7 && distance < 9) {
    signalAndSwitchSend(102, STRAIGHT);
    stopTrain(8, GLIDE);
    startTrain(40, "forward", 8);
    startTrain(40, "forward", 8);
    Serial.print("Distance: ");
    Serial.println(distance);
    delay(500);
  }
}
