#include "h/fmsynth.h"

// Constructor & Destructor
FMSynth::FMSynth(float frequency, float ratio, int samplerate) : Synth() {
  setFrequency(frequency);
  setPhaseStep(frequency / samplerate);
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
// Phase step setter
void FMSynth::setPhaseStep(float phase_step) {
  this->phase_step = phase_step;
}
// Phase step getter
float FMSynth::getPhaseStep() {
  return phase_step;
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
  float freq = Synth::mtof(note);
  setFrequency(freq);
  voice_pointer->setFrequency(freq);
  mod_pointer->setFrequency(freq * ratio);
}

// Calculate sample via modulation
float FMSynth::getSample() {
  float mod = mod_pointer->getSample() * getModIndex() * 0.01;
  voice_pointer->setPhaseStep(phase_step + mod);
  voice_pointer->next();
  return voice_pointer->getSample() * amplitude;
}
