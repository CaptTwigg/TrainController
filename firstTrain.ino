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
  STRAIGHT,
  TURN
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
char track = 154;
char left = 251;
char left2 = 243;
char right = 250;
char right2 = 242;
int looping =0;



void setup()
{
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(DCC_PIN, OUTPUT);      // enable styrepin som output
  //pinMode(dirpin,INPUT_PULLUP);// dirpin som input
  SetupTimer2();

  addr      = locoAddr;          // default lokoadresse
  data      = locoSpeed;         // default hastighed og retning, rew speed = 4


  pinMode(LED_BUILTIN, OUTPUT);


}

void loop()
{
 

  if (Serial.available()) {
    String dataset = Serial.readString();
    Serial.println("python: " + dataset);

    if (dataset.equals("blink")) {
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    }
    if (dataset.equals("noblink")) {
      digitalWrite(LED_BUILTIN, LOW);   // turn the LED on (HIGH is the voltage level)
    }

    if(dataset.startsWith("train")){
      Serial.println(strtok(dataset))
      
      
    }
    // Serial.println(dataset);
  }

  //startTrain(9, "back", 0xf);

  //delay(1000);

  //stopTrain(9, GLIDE);

  //delay(3000);

  //trainSwitch(track,TURN);
  //delay(2000);
  //trainSwitch(track,STRAIGHT);




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

void trainSwitch(int track, char Direction) {

  if (Direction == TURN) {
    assemble_dcc_msg(track, left);
    delay(50);
    assemble_dcc_msg(track, left2);
    delay(50);
  } else {
    assemble_dcc_msg(track, right);
    delay(50);
    assemble_dcc_msg(track, right2);
    delay(50);
  }

}
