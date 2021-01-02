#pragma once
#include "osc.h"

class Sine : public Oscillator {
  public:
    Sine(float frequency);
    ~Sine();

    float next();
};
