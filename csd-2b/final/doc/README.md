# noise thing
noise thing is a simple fixed two-voice synthesizer program that runs from your terminal. It's written in C++ and uses JACK as an audio backend.

## Commands
#### `play`
The `play` command opens an interactive shell where the user can type MIDI note values to play the synth.

#### `melody`
The `melody` toolkit contains two utilities for using melodies in noise thing. With `melody generate`, a user can generate a melody of any given length. This melody can then be played using the `melody play` command.

#### `solo`
With `solo`, users can solo each of the two fixed synth voices by typing `solo [voice]`. To hear all voices again, one can use the `solo reset` command.

#### `help`
The `help` command prints a short overview of all available commands.