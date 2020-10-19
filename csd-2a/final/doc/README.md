# NeuroBeat
### Introduction
NeuroBeat is a simple ML-based beat generation algorithm written in Python. The full process, from training models to playing back rhythms, was written from the ground up. No existing ML libraries have been used.

### Contents
1. [Basic Usage](#basic-usage)
1. [Training Models](#training-models)
1. [Generating Rhythms](#generating-rhythms)
1. [Playing back Rhythms](#playing-back-rhythms)
1. [Exporting Rhythms](#exporting-rhythms)

### Dependencies
NeuroBeat depends on the following non-standard packages (installation via `pip3`):
- `mido`
- `termcolor`
- `python-rtmidi`

## Basic Usage
To use the program, clone this repo first. Then, navigate to `/src` and run `python3 main.py`. `main.py` serves as an entry point for the application. Use `help` to list all available commands, `about` to show the about text and `exit` to close the program.

## Training Models
To train a model, first make sure that there are source MIDI files available for the training algorithm to use. These files should be placed in `/train/{ LIBRARY }/{ TIME_SIGNATURE }`. The value of `{ LIBRARY }` is arbitrary. The time signature folder should be named according to the convention `{ UPPER }-{ LOWER }`.

Once a decent amount of files is present in the desired training directory, run the program and execute the `train` command. Enter the time signature you want to train for, as well as the `{ LIBRARY }` (or "dataset") you created in the first step. The program will now train and store a model based on the user input.

## Generating Rhythms
Before generating a rhythm, make sure you have at least one trained model in the `/model` folder. If not, please see [Training Models](#training-models) for more info.

To get started, run the `generate` command. Enter the desired time signature (this should match any of your trained models), as well as a length for the rhythm, the dataset to take the model from, and options for humanization. The program will now generate a rhythm based on the stored model.

## Playing back Rhythms
After generating a rhythm, you can now play it back. To start the player, run the `play` command. Within the player environment, the following commands are available to you:
- `play`: start playback
- `stop`: stop playback and return to the main program
- `loop`: toggle looping (turned off by default)
- `bpm { BPM }`: change the playback BPM
- `interface`: select the MIDI interface to use
- `help`: show a list of available commands

## Exporting Rhythms
To export the latest generated rhythm, run the `export` command. This will write the rhythm to a MIDI file that is stored in the `/export` directory.