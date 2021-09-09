 #include "AccelStepper.h"

#define dirPin 2
#define stepPin 5
#define motorInterfaceType 1

int interrupt_sens = A0;

int hom = 0;

AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

void go_to_home(){
  stepper.setSpeed(4000);
  while(sensor() <600){
    stepper.move(-1000);
    stepper.runSpeedToPosition();
  }
  stepper.setCurrentPosition(0);
}

int sensor(){
  return analogRead(interrupt_sens);
}

void setup() {
  Serial.begin(9600);
  stepper.setMaxSpeed(2000);
  stepper.setAcceleration(500);
  go_to_home();
}

void loop() {

  while (Serial.available() > 0) {
    
    String str = Serial.readString();
    
    if(str.startsWith("is")){
      Serial.print("sensor val: ");
      Serial.println(sensor());
    }
    else if(str.startsWith("home")){
      go_to_home();
      Serial.println("done");
    }
    else if(str.startsWith("ma")){
      long int pos = str.substring(2).toInt();
//      Serial.print("ma: "); Serial.println(pos);
      stepper.moveTo(pos);
      stepper.runToPosition();
      Serial.println("done");
    }
    else if (str.startsWith("mr")){
      stepper.setSpeed(2000);
      long int pos = str.substring(2).toInt();
      Serial.print("mr: "); Serial.println(pos);
      stepper.move(pos);
      stepper.runSpeedToPosition();
//      while (stepper.currentPosition() != stepper.targetPosition()) {
//        Serial.print("current pos:"); Serial.println(stepper.currentPosition());
//        Serial.print("target pos:");  Serial.println(stepper.targetPosition());
//        stepper.runSpeedToPosition();
//      }
    }
    else{
      Serial.println("Invalid Option!");
    }
  }
}
