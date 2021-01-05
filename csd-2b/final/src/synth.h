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
    Synth();
    ~Synth();

    static float mtof(int note);

  protected:
    // Envelope envelope;

    int samplerate;
};
