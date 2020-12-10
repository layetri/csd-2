#include <iostream>
#include "instrument.h"

int main() {
  Instrument instr1("test\n");
  Instrument instr2("test2\n");

  instr1.play();
  instr2.play();
}
