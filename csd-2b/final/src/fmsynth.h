//
// Created by Daniël Kamp on 04/01/2021.
//

#pragma once
#include "synth.h"

class FMSynth {
  public:
    FMSynth(float frequency, float ratio, int samplerate);
    ~FMSynth();

    // Ratio functions
    void setRatio(float ratio);

    // Frequency functions
    void setFrequency(float frequency);
    float getFrequency();

    // Modulation functions
    void setModIndex(float mod_index);
    float getModIndex();

    // Transport functions
    void next();
    float getSample();
    void play(int note);

  protected:
    Oscillator *voice_pointer = nullptr;
    Oscillator *mod_pointer = nullptr;
    float ratio;
    float mod_index;
    float frequency;
};
