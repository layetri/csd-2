#include "osc.h"
#include <iostream>

// Constructor
Oscillator::Oscillator(float frequency, int samplerate) {
  // Initialize variables
  setFrequency(frequency);
  setSamplerate(samplerate);
  amplitude = 0.2;
  phase = 0;
}

// Destructor
Oscillator::~Oscillator() {}

// Buffer the waveform
void Oscillator::buffer() {

}

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

// Phase getter
float Oscillator::getPhase() {
  return phase;
}

// Phase increment
void Oscillator::incrementPhase() {
  phase += phase_step;
  if(phase > 1.0) phase -= 1.0;

//  std::cout << phase << std::endl << phase_step << std::endl;
}

// GetSample dummy
float Oscillator::getSample() {
  return 0.0;
}
// Next dummy
void Oscillator::next() {}