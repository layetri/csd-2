instrument: instrument.o main.o
	g++ -o instrument instrument.o main.o


instrument.o: instrument.cpp instrument.h
	g++ -std=c++11 -c instrument.cpp


main.o: main.cpp instrument.h
	g++ -std=c++11 -c main.cpp


clean:
	rm instrument *.o
