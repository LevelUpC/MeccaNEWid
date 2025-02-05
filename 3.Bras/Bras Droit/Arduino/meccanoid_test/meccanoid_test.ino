#include <Meccanoid.h>

typedef MeccanoServo Servo;
typedef MeccanoLed   Led;

int pin = 3;
Chain chain(pin);

Servo servo1 = chain.getServo(0); // premier servo sur la chaîne (0)
Servo servo2 = chain.getServo(1); // deuxième servo sur la chaîne (1)

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Actualise la chaîne pour la mise à jour des modules
  chain.update();

  // Si une commande est disponible sur le port série
  if (Serial.available() > 0) {
    // Lecture jusqu'au saut de ligne
    String input = Serial.readStringUntil('\n');
    input.trim(); // supprime les espaces superflus
    if (input.length() > 0) {
      // On attend deux nombres séparés par un espace
      int separator = input.indexOf(' ');
      if (separator > 0) {
        int pos1 = input.substring(0, separator).toInt();
        int pos2 = input.substring(separator + 1).toInt();
        // Affecte les positions lues aux servos
        servo1.setPosition(pos1);
        servo2.setPosition(pos2);
      }
    }
  }
}
