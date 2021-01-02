#include "sqr.h"
#include <math.h>

Square::Square(float frequency) : Oscillator(frequency) {

}

Square::~Square() {

}

float Square::next() {
  incrementPhase();
  float val;
  int harmonics = 10;

  for(int i = 1; i < harmonics; i++) {
    int n = (2 * i) - 1;
    val += sin(TWO_PI * n * getPhase()) / n;
  }

  return val;
}
