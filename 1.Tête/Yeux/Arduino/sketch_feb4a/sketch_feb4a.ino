#include <Meccanoid.h>

typedef MeccanoLed Led;

int pin = 3;
Chain chain(pin);
Led eyes = chain.getLed(0);

void setup() {
    Serial.begin(9600);
}

void loop() {
    // Mise à jour de la chaîne pour actualiser les modules
    chain.update();
    
    // Si au moins trois octets sont disponibles, on lit les valeurs RGB
    if (Serial.available() >= 3) {
        byte r = Serial.read();
        byte g = Serial.read();
        byte b = Serial.read();
        eyes.setColor(r, g, b, 0);
    }
}
