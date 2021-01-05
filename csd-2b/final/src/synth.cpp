//
// Created by Daniël Kamp on 03/01/2021.
//

#include "h/synth.h"

Synth::Synth() {
  amplitude = 0.3;
}

Synth::~Synth() {}

// Amplitude setter
void Synth::setAmplitude(float amplitude) {
  // Make sure we can't go too loud
  if(amplitude > 1.0) {
    this->amplitude = 1.0;
  } else {
    this->amplitude = amplitude;
  }
}

float Synth::mtof(int note) {
  return pow(2.0, (note - 69.0) / 12.0) * 440.0;
}