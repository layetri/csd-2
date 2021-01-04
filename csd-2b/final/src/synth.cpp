//
// Created by Daniël Kamp on 03/01/2021.
//

#include <math.h>
#include <fstream>
#include <iostream>

#include "synth.h"

Synth::Synth(std::string voice_type, int samplerate) {
  this->samplerate = samplerate;

  if(voice_type.compare("square") == 0) {
    //Square voice(440.0, samplerate);
    voice_pointer = new Square(440.0, samplerate);
  } else if(voice_type == "sine") {
    voice_pointer = new Sine(440.0, samplerate);
  } else if(voice_type == "tri") {
    voice_pointer = new Triangle(440.0, samplerate);
  }
}

Synth::~Synth() {
  delete voice_pointer;
}

float Synth::mtof(int note) {
  return pow(2.0, (note - 69.0) / 12.0) * 440.0;
}

float Synth::getSample() {
  return voice_pointer->getSample();
}

void Synth::next() {
  voice_pointer->next();
}

void Synth::play(int note) {
  float frequency = mtof(note);
  float buffer[samplerate];

  voice_pointer->setFrequency(frequency);

  // Write data to file
//  std::ofstream dump;
//  dump.open ("dump.csv");
//
//  for(int i = 0; i < samplerate; i++) {
//    //buffer[i] = voice.next();
//    //dump << buffer[i] << std::endl;
//  }
//
//  dump.close();
}