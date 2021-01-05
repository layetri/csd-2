//
// Created by Daniël Kamp on 03/01/2021.
//

#include <math.h>
#include <fstream>
#include <iostream>

#include "synth.h"

Synth::Synth() {}

Synth::~Synth() {}

float Synth::mtof(int note) {
  return pow(2.0, (note - 69.0) / 12.0) * 440.0;
}