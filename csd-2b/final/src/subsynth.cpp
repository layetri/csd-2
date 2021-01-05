//
// Created by Daniël Kamp on 04/01/2021.
//

#include "h/subsynth.h"
#include <stdexcept>

SubSynth::SubSynth(float frequency, std::string waveform, int samplerate) : Synth() {
  this->samplerate = samplerate;

  if(waveform == "square") {
    voice_pointer = new Square(frequency, samplerate);
  } else if(waveform == "sine") {
    voice_pointer = new Sine(frequency, samplerate);
  } else if(waveform == "tri") {
    voice_pointer = new Triangle(frequency, samplerate);
  } else {
    throw std::invalid_argument("This is not a waveform!");
  }
}

SubSynth::~SubSynth() {
  delete voice_pointer;
}

float SubSynth::getSample() {
  return voice_pointer->getSample() * amplitude;
}

void SubSynth::next() {
  voice_pointer->next();
}

void SubSynth::play(int note) {
  float freq = Synth::mtof(note);
  voice_pointer->setFrequency(freq);
}
