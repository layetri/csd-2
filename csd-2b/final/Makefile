CC=g++
SRC_DIR=src
OBJ_DIR=obj
SOURCES=$(wildcard $(SRC_DIR)/*.cpp)
OBJECTS=$(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(SOURCES))

# Link all
synth: $(OBJECTS)
	$(CC) -o $@ $^

# Separate rule for main.cpp since it doesn't have a header
obj/main.o: src/main.cpp
	$(CC) -c -std=c++11 $< -o $@

# Make all .cpp source files into .o files
obj/%.o: src/%.cpp src/%.h
	$(CC) -c -std=c++11 $< -o $@

# Install to system path
install:
	mv synth /usr/var/bin/

# Clean up
clean:
	rm synth *.o