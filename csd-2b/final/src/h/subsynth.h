//
// Created by Daniël Kamp on 04/01/2021.
//

#pragma once
#include "synth.h"
#include "osc.h"
#include "sqr.h"
#include "sin.h"
#include "tri.h"

#include <string>
#include <math.h>

class SubSynth : public Synth {
  public:
    SubSynth(float frequency, std::string waveform, int samplerate);
    ~SubSynth();

    // Transport functions
    void next();
    float getSample();
    void play(int note);
  protected:
    Oscillator *voice_pointer = nullptr;
    int samplerate;
};
