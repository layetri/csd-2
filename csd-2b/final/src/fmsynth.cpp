#include "fmsynth.h"

// Constructor & Destructor
FMSynth::FMSynth(float frequency, float ratio, int samplerate) {
  setFrequency(frequency);
  setRatio(ratio);
  setModIndex(1.0);
  voice_pointer = new Sine(frequency, samplerate);
  mod_pointer = new Sine(frequency * ratio, samplerate);
}

FMSynth::~FMSynth() {
  delete voice_pointer;
  delete mod_pointer;
}

// Ratio setter
void FMSynth::setRatio(float ratio) {
  this->ratio = ratio;
}
// Frequency setter
void FMSynth::setFrequency(float frequency) {
  this->frequency = frequency;
}
// Frequency getter
float FMSynth::getFrequency() {
  return frequency;
}
// Mod index setter
void FMSynth::setModIndex(float mod_index) {
  this->mod_index = mod_index;
}
// Mod index getter
float FMSynth::getModIndex() {
  return mod_index;
}

// Tick next on child processes
void FMSynth::next() {
  mod_pointer->next();
}

// Set note properties
void FMSynth::play(int note) {
  setFrequency(Synth::mtof(note));
}

// Calculate sample via modulation
float FMSynth::getSample() {
  float mod = mod_pointer->getSample() * getModIndex();
  voice_pointer->setFrequency(frequency + mod);
  return voice_pointer->getSample();
}
