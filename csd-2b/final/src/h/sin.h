#pragma once
#include "osc.h"

class Sine : public Oscillator {
  public:
    Sine(float frequency, int samplerate);
    ~Sine();

    float getSample() override;
    void next() override;

  private:
    float sample;
};
