#include "sin.h"
#include <math.h>
#include <iostream>

Sine::Sine(float frequency, int samplerate) : Oscillator(frequency, samplerate) {}

Sine::~Sine() {}

float Sine::getSample() {
  return sample;
}

void Sine::next() {
  incrementPhase();
  sample = sin(TWO_PI * getPhase());
}
