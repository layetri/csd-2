#include <iostream>
#include "instrument.h"

// Constructor & Destructor methods
Instrument::Instrument(std::string new_sound) {
  sound=new_sound;
}

Instrument::~Instrument() {

}

// Function definitions
void Instrument::play() {
  std::cout << sound;
}
