#include "h/tri.h"

Triangle::Triangle(float frequency, int samplerate) : Oscillator(frequency, samplerate) {

}

Triangle::~Triangle() {

}

float Triangle::getSample() {
  return sample;
}

void Triangle::next() {
  incrementPhase();
  sample = asin(sin(TWO_PI * getPhase()));
}