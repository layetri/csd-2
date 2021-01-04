//
// Created by Daniël Kamp on 04/01/2021.
//

#include "subsynth.h"
#include <iostream>

SubSynth::SubSynth(float frequency, std::string waveform, int samplerate) {
  this->samplerate = samplerate;

  if(waveform == "square") {
    voice_pointer = new Square(frequency, samplerate);
  } else if(waveform == "sine") {
    voice_pointer = new Sine(frequency, samplerate);
  } else if(waveform == "tri") {
    voice_pointer = new Triangle(frequency, samplerate);
  }
}

SubSynth::~SubSynth() {
  std::cout << "Deleting SubSynth voice\n";
  delete voice_pointer;
}

float SubSynth::getSample() {
  std::cout << "Subsynth called at " << voice_pointer << std::endl;
  std::cout << voice_pointer->getSample();
  // THE PROBLEM STARTS HERE
  return voice_pointer->getSample();
}

void SubSynth::next() {
  voice_pointer->next();
}

void SubSynth::play(int note) {
  //float frequency = Synth::mtof(note);
  //voice_pointer->setFrequency(frequency);
}
