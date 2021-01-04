#pragma once
#include "osc.h"

class Triangle : public Oscillator {
  public:
    Triangle(float frequency, int samplerate);
    ~Triangle();

    float getSample() override;
    void next() override;

  private:
    float sample;
};