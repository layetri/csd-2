//
// Created by Daniël Kamp on 03/01/2021.
//

#include "h/melody.h"

Melody::Melody(int length) {
  this->length = length;

  int choices[12] = {0, 2, 3, 5, 7, 8, 11, 12, 14, 15, -1, -4};
  int root = (rand() % 48) + 36;

  for(int i = 0; i < length - 1; i++) {
    melody.push_back(choices[rand() % 12] + root);
  }
  // Make sure the melody ends on the root note
  melody.push_back(root);
}

Melody::~Melody() {}

int Melody::getLength() const {
  return length;
}

int Melody::shift(int places) {
  return melody[places];
}