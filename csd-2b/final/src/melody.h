//
// Created by Daniël Kamp on 03/01/2021.
//

#pragma once

class Melody {
  public:
    explicit Melody(int length);
    ~Melody();

    void play();

    int melody;
  private:
    int length;

    int generate(int length);
};