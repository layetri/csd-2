//
// Created by Daniël Kamp on 03/01/2021.
//

#pragma once
#include <vector>
#include <cstdlib>

class Melody {
  public:
    explicit Melody(int length);
    ~Melody();

    int getLength() const;
    int shift(int places);

    std::vector<int> melody;
    int *melody_pointer;
  private:
    int length;
};