//
// Created by Daniël Kamp on 03/01/2021.
//

#pragma once
#include <string>
#include <math.h>

#include "osc.h"
#include "sqr.h"
#include "sin.h"
#include "tri.h"

class Synth {
  public:
    Synth();
    ~Synth();

    static float mtof(int note);
    void setAmplitude(float amplitude);

  protected:
    int samplerate;
    float amplitude;
};
