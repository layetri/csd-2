#include "sin.h"
#include <math.h>

Sine::Sine(float frequency) : Oscillator(frequency) {

}

Sine::~Sine() {

}

float Sine::next() {
  incrementPhase();
  return sin(TWO_PI * getPhase());
}
