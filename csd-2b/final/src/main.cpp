#include <iostream>
#include <fstream>

#include "osc.h"
#include "sin.h"
#include "sqr.h"

float buffer[SAMPLERATE];

int main() {
  Square sine(2);

  std::ofstream dump;
  dump.open ("dump.csv");

  for(int i = 0; i < SAMPLERATE; i++) {
    buffer[i] = sine.next();
    dump << buffer[i] << std::endl;
  }

  dump.close();

  std::cout << buffer[1024] << std::endl;
}
