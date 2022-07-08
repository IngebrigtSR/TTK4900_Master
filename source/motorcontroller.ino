/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <torgeir@selbu.org> wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.   Torgeir Leithe
 * ----------------------------------------------------------------------------
 */
#include <Servo.h>

//TODO Find correct value
int maxValueServo = 2000;
int minValueServo = 1010;

int minValueUART = 9;
int maxValueUART = 56;

int servoPin1 = 9;
int servoPin2 = 10;
int servoPin3 = 11;
int servoPin4 = 6;

Servo Servo1;
Servo Servo2;
Servo Servo3;
Servo Servo4;

void setup() {

// Configure UART, 115200 baud
  Serial.begin(115200);
  Serial.setTimeout(10000000);
  
Servo1.attach(servoPin1);
Servo2.attach(servoPin2);
Servo3.attach(servoPin3);
Servo4.attach(servoPin4);

}

void loop() {

  // Get input values
  int ServoValueUART1 = Serial.parseInt();
  int ServoValueUART2 = Serial.parseInt();
  int ServoValueUART3 = Serial.parseInt();
  int ServoValueUART4 = Serial.parseInt();

  // Resync with host
  Serial.readStringUntil('\n');
   
  //Scale inputvalues from minValueUART to maxValueUART, to minValueServo to maxValueServo
  int ServoValue1 = map(ServoValueUART1, minValueUART, maxValueUART, minValueServo, maxValueServo);
  int ServoValue2 = map(ServoValueUART2, minValueUART, maxValueUART, minValueServo, maxValueServo);
  int ServoValue3 = map(ServoValueUART3, minValueUART, maxValueUART, minValueServo, maxValueServo);
  int ServoValue4 = map(ServoValueUART4, minValueUART, maxValueUART, minValueServo, maxValueServo);

Servo1.writeMicroseconds(ServoValue1);
Servo2.writeMicroseconds(ServoValue2);
Servo3.writeMicroseconds(ServoValue3);
Servo4.writeMicroseconds(ServoValue4);

  // Output used values
  Serial.print(ServoValue1);
  Serial.print(" ");
  Serial.print(ServoValue2);
  Serial.print(" ");
  Serial.print(ServoValue3);
  Serial.print(" ");
  Serial.print(ServoValue4);
  Serial.print("\r\n");
}

