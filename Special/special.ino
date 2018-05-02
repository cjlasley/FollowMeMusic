int pastLevels[10];

void setup() {
  Serial.begin(1000000);
  while (!Serial){;}
}

void loop() {
  // Serial protocol:
  // >PIN:LEVEL;
  if (Serial.find(">")) {
    int pin = Serial.parseInt();
    if(Serial.find(":")) {
      int level = Serial.parseInt();
      if (Serial.find(";")) {
        updateLights(level);
        // analogWrite(pin, level);
        char buf[50];
        sprintf(buf, "Wrote %d to %d\n", level, pin);
        Serial.write(buf);
      }
    }
  }
}

void updateLights(int newLevel) {
  pastLevels[0] = newLevel;
  for (int i=0; i < 10; ++i) {
    analogWrite(i + 2, pastLevels[i]);
    pastLevels[i + 1] = pastLevels[i];
  }
}
