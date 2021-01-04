//
// Created by Daniël Kamp on 03/01/2021.
//

#pragma once

class Melody {
  public:
    explicit Melody(int length);
    ~Melody();

    static void play();
    static bool assure();
    static int instances;

    int melody;
  private:
    int generate(int length);
};