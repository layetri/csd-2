//
// Created by Daniël Kamp on 03/01/2021.
//

#pragma once
#include <string>

#include "osc.h"
#include "sqr.h"
#include "sin.h"
#include "tri.h"

class Synth {
  public:
    Synth(std::string voice_type, int samplerate);
    ~Synth();

    void play(int note);
    void next();
    float getSample();

  protected:
    __unused Oscillator *voice_pointer = nullptr;
    // Envelope envelope;

    int samplerate;
    float mtof(int note);
};
