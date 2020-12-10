#! /bin/bash

g++ -c main.cpp
g++ -c instrument.cpp
g++ -o output/instrument main.o instrument.o
