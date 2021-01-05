#include "h/sqr.h"

Square::Square(float frequency, int samplerate) : Oscillator(frequency, samplerate) {

}

Square::~Square() {

}

float Square::getSample() {
  return sample;
}

void Square::next() {
  incrementPhase();
  sample = 0.0;
  int harmonics = 10;

  for(int i = 1; i < harmonics; i++) {
    int n = (2 * i) - 1;
    sample += sin(TWO_PI * n * getPhase()) / n;
  }
}
