#include "osc.h"
#include <iostream>

// Constructor
Oscillator::Oscillator(float frequency) {
  std::cout << "Booting oscillator" << std::endl;
  // Initialize variables
  setFrequency(frequency);
  amplitude = 0.2;
  phase = 0;
  sample = 0;
}

// Destructor
Oscillator::~Oscillator() {
  std::cout << "Cleaning up oscillator" << std::endl;
}

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

// Phase step calculator
void Oscillator::calculatePhaseStep() {
  phase_step = frequency / SAMPLERATE;
  std::cout << std::to_string(phase_step) << std::endl;
}

// Phase getter
float Oscillator::getPhase() {
  return phase;
}

void Oscillator::incrementPhase() {
  phase += phase_step;

  if(phase > 1.0) phase -= 1.0;
}