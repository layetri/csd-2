#include "h/osc.h"

// Constructor
Oscillator::Oscillator(float frequency, int samplerate) {
  // Initialize variables
  this->frequency = frequency;
  this->samplerate = samplerate;
  amplitude = 0.2;
  phase = 0;

  calculatePhaseStep();
}

// Destructor
Oscillator::~Oscillator() {}

// Frequency getter
float Oscillator::getFrequency() {
  return frequency;
}

// Frequency setter
void Oscillator::setFrequency(float frequency) {
  this->frequency = frequency;
  calculatePhaseStep();
}

// Amplitude getter
float Oscillator::getAmplitude() {
  return amplitude;
}

// Amplitude setter
void Oscillator::setAmplitude(float amplitude) {
  this->amplitude = amplitude;
}

// Samplerate getter
double Oscillator::getSamplerate() {
  return samplerate;
}

// Amplitude setter
void Oscillator::setSamplerate(int samplerate) {
  this->samplerate = samplerate;
  calculatePhaseStep();
}

// Phase step calculator
void Oscillator::calculatePhaseStep() {
  phase_step = frequency / samplerate;
}

void Oscillator::setPhaseStep(float phase_step) {
  this->phase_step = phase_step;
}

// Phase getter
float Oscillator::getPhase() {
  return phase;
}

// Phase increment
void Oscillator::incrementPhase() {
  phase += phase_step;
  if(phase > 1.0) phase -= 1.0;
}

// GetSample dummy
float Oscillator::getSample() {
  return 0.0;
}
// Next dummy
void Oscillator::next() {}