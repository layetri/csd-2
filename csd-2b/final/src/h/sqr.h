#pragma once
#include "osc.h"

class Square : public Oscillator {
  public:
    Square(float frequency, int samplerate);
    ~Square();

    float getSample() override;
    void next() override;

  private:
    float sample;
};