#include <Arduino.h>

#define RED 11  // RGB LED pins
#define BLUE 10 //
#define GREEN 9 //

#define LDR A0 // LDR pin - analog

#define DELAY 50 // Time between color shift, in micro seconds

unsigned long old_time_index = 0; // Global indexing
unsigned long global_index = 0;   //

float ALPHA = 0.95f; // Alpha value for complimentaty filter

unsigned int current_value = 0; // Keep track of values for complimentary filter
unsigned int previous_value = 0; //

unsigned int r, g, b; // Global color values

void setup(void) {
  // Define RGB pins
  pinMode(RED, OUTPUT);
  pinMode(BLUE, OUTPUT);
  pinMode(GREEN, OUTPUT);

  // Define LDR pin
  pinMode(LDR, INPUT);

  Serial.begin(115200);

  delay(100);

  old_time_index = micros();
}

void shift_light() {
  const float alpha_ = 0.001;

  unsigned long offset_r = 0;
  unsigned long offset_g = 250000;
  unsigned long offset_b = 500000;

  // r = (sin((global_index + offset_r) * alpha_)) * 127.5 + 127.5;
  // g = (sin((global_index + offset_g) * alpha_)) * 127.5 + 127.5;
  b = (sin((global_index + offset_b) * alpha_)) * 127.5 + 127.5;
}

void light() {
  analogWrite(RED, r);
  analogWrite(GREEN, g);
  analogWrite(BLUE, b);
}

void read() {
  int readVal = (analogRead(LDR) * ALPHA) + (previous_value * (1.0f - ALPHA));
  previous_value = analogRead(LDR);

  Serial.println(String(r) + "," + String(g) + "," + String(b) + "," +
                 String(readVal));
}

void loop() {
  if (micros() - old_time_index >= DELAY) {
    old_time_index = micros();
    global_index += 1;
  }

  shift_light();
  light();
  read();
}