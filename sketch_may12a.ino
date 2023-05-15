#include <Servo.h>
int data_x1 = 0;
int data_y1 = 0;
int data[1];
Servo myservo_x1;
Servo myservo_y1;// create servo object to control a servo
// twelve servo objects can be created on most boards

//int pos = 0;    // variable to store the servo position

void setup() {
  Serial.begin(9600);
  myservo_x1.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo_y1.attach(10);
  myservo_x1.write(90);
  myservo_y1.write(90);
}

void loop() {
  while (Serial.available() >= 2) {
    //    data_x1=Serial.read();
    //    data_y1=Serial.read();
    for (int i = 0; i < 2; i++) {
      data[i] = Serial.read();
    }

    myservo_x1.write(data[0]);
    myservo_y1.write(data[1]);

    Serial.println(data[0]);
    Serial.println(data[1]);
  }
  
}
