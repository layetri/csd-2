//
// Created by Daniël Kamp on 03/01/2021.
//

#include "melody.h"
#include <cstdlib>
#include <iostream>

Melody::Melody(int length) {
  instances++;
  melody = generate(length);
}

Melody::~Melody() {
  instances--;
}

int Melody::generate(int length) {
  int mel[length];
  int *melody_pointer = mel;
  int choices[12] = {0, 2, 3, 5, 7, 8, 11, 12, 14, 15, -1, -4};
  int root = (rand() % 48) + 24;

  for(int i = 0; i < length; i++) {
    mel[i] = choices[rand() % 12] + root;
  }

  return *melody_pointer;
}

void Melody::play() {

}

bool Melody::assure() {
  return instances > 0;
}
