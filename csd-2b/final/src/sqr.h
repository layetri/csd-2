#pragma once
#include "osc.h"

class Square : public Oscillator {
  public:
    Square(float frequency);
    ~Square();

    float next();
};