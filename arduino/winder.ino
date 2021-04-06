//**************************************************************
// Driver ULN2003, motor reduced to 1:64
//**************************************************************

#include <Stepper.h>
// LED
#define LED 5

// Motor
#define STEPS 100
// Speed
// max 300, maybe >300 vibration problems and no turning
#define SPEED 250
// Arduino pins
// Stepper pins 1 2 3 4 to DOs 8 9 10 11 of Arduino (incl. GND, +V)
// clockwise, counter clockwise: change 8 + 11
#define M1 8
#define M2 10
#define M3 9
#define M4 11

// loop values
#define LOOP 20
#define WAIT 120
#define DELAY 1000
#define MOTOR_STEPS 4096

// Init instance of stepper
Stepper motor(STEPS, M1, M2, M3, M4);

int steps2take = 0; // required motor steps
long msTime = 0; // time for 1 round
int counter;

//************************************************************
// 64 steps per round, 4 phases, 5,625° angle
// Relation 1:64
// 360° / 5.625° * 64 = 4096 angles
// 360° / 5.625° * 64 * 4 coins/ 2 bipols = 2048 step / round
//************************************************************

void setup() {
  Serial.begin(9600); // open the serial port at 9600 bps:
  Serial.println("Init stepper program");
  pinMode(LED, OUTPUT); // Set LED pin
}

void loop() {
  digitalWrite(LED, HIGH);
  delay(100);
  if (counter > 0) {
    Serial.println(String(counter) + String(".loop done"));
  }
  else if (counter > LOOP){
    Serial.println(String(counter) + String(".loop w/o turns"));
  }

  motor.setSpeed(SPEED);

  if (counter < LOOP) { // LOOP*2 turns (each 2 clockwise and 2 counter clockwise)
      Serial.println("<---- counter clockwise");
      turn(-1 * MOTOR_STEPS);
      delay(DELAY);
      Serial.println("----> clockwise");
      turn(MOTOR_STEPS);
      delay(DELAY);
      oneSecondBlink();
      counter++;
    }
  else if (counter < WAIT) { // 1200 seconds (20 minutes) standby
    Serial.println("Waiting...");
    for (int x = 0; x < 10; x++) {
      oneSecondBlink();
    }
    counter++;
  }
  else {
    counter = 0;
  }
}

String turnTimeString(int timeValue) {
  return (String("duration: ") + String(timeValue / 1000.000, 3) + String(" sec"));
}

void turn(int steps) {
  steps2take = steps;
  // 1 round with 2048 steps
  // for 6 times 1/30 round counter clockwise, e.g. steps2take = -6 * 2048 / 30
  msTime = millis();
  motor.step(steps2take); // turn assignment
  msTime = millis() - msTime ; // 6,236 sec per round if speed 200
  Serial.println(turnTimeString(msTime)); // per full loop
}

void oneSecondBlink() {
  digitalWrite(LED, LOW);
  delay(800);
  digitalWrite(LED, HIGH);
  delay(200);
}