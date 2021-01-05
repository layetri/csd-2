//
// Noise Thing v1.0
// © 2021 Daniël Kamp
//

// Include libraries
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include "h/jack_module.h"

// Include program headers
#include "h/subsynth.h"
#include "h/fmsynth.h"
#include "h/melody.h"

// Use std namespace instead of std-littering our code
using namespace std;

// Abstraction to easily provide a text coloring utility
string color(string text, int color) {
  return "\033[" + to_string(color) + "m" + text + "\033[0m";
}

// Input integer validation (borrowed from https://stackoverflow.com/questions/2844817/how-do-i-check-if-a-c-string-is-an-int/37864920 (and yes, I upvoted!))
inline bool isInteger(const std::string & s)
{
  if(s.empty() || ((!isdigit(s[0])) && (s[0] != '-') && (s[0] != '+'))) return false;

  char * p;
  strtol(s.c_str(), &p, 10);

  return (*p == 0);
}

// Printing the logo
void printLogo() {
  cout << color("      ___           ___                       ___           ___     \n", 36) <<
       color("     /\\__\\         /\\  \\          ___        /\\  \\         /\\  \\    \n", 36) <<
       color("    /::|  |       /::\\  \\        /\\  \\      /::\\  \\       /::\\  \\   \n", 36) <<
       color("   /:|:|  |      /:/\\:\\  \\       \\:\\  \\    /:/\\ \\  \\     /:/\\:\\  \\  \n", 36) <<
       color("  /:/|:|  |__   /:/  \\:\\  \\      /::\\__\\  _\\:\\~\\ \\  \\   /::\\~\\:\\  \\ \n", 36) <<
       color(" /:/ |:| /\\__\\ /:/__/ \\:\\__\\  __/:/\\/__/ /\\ \\:\\ \\ \\__\\ /:/\\:\\ \\:\\__\\\n", 36) <<
       color(" \\/__|:|/:/  / \\:\\  \\ /:/  / /\\/:/  /    \\:\\ \\:\\ \\/__/ \\:\\~\\:\\ \\/__/\n", 36) <<
       color("     |:/:/  /   \\:\\  /:/  /  \\::/__/      \\:\\ \\:\\__\\    \\:\\ \\:\\__\\  \n", 36) <<
       color("     |::/  /     \\:\\/:/  /    \\:\\__\\       \\:\\/:/  /     \\:\\ \\/__/  \n", 36) <<
       color("     /:/  /       \\::/  /      \\/__/        \\::/  /       \\:\\__\\    \n", 36) <<
       color("     \\/__/         \\/__/                     \\/__/         \\/__/    \n\n", 36);
  cout << color("      ___           ___                       ___           ___     \n", 35) <<
       color("     /\\  \\         /\\__\\          ___        /\\__\\         /\\  \\    \n", 35) <<
       color("     \\:\\  \\       /:/  /         /\\  \\      /::|  |       /::\\  \\   \n", 35) <<
       color("      \\:\\  \\     /:/__/          \\:\\  \\    /:|:|  |      /:/\\:\\  \\  \n", 35) <<
       color("      /::\\  \\   /::\\  \\ ___      /::\\__\\  /:/|:|  |__   /:/  \\:\\  \\ \n", 35) <<
       color("     /:/\\:\\__\\ /:/\\:\\  /\\__\\  __/:/\\/__/ /:/ |:| /\\__\\ /:/__/_\\:\\__\\\n", 35) <<
       color("    /:/  \\/__/ \\/__\\:\\/:/  / /\\/:/  /    \\/__|:|/:/  / \\:\\  /\\ \\/__/\n", 35) <<
       color("   /:/  /           \\::/  /  \\::/__/         |:/:/  /   \\:\\ \\:\\__\\  \n", 35) <<
       color("   \\/__/            /:/  /    \\:\\__\\         |::/  /     \\:\\/:/  /  \n", 35) <<
       color("                   /:/  /      \\/__/         /:/  /       \\::/  /   \n", 35) <<
       color("                   \\/__/                     \\/__/         \\/__/    \n\n", 35);
}

// Initialize melody vector
vector<Melody> melodies;

// Main program loop
int main(int argc, char* argv[]) {
  JackModule jack;
  jack.init(argv[0]);
  int samplerate = jack.getSamplerate();
  if(samplerate == 0) {
    samplerate = 44100;
  }

  // Initialize melody player variables
  bool playing = false;
  int melody_new_note = 0;

  // Print the welcome screen ✨
  printLogo();
  cout << color("System says: ", 32) << "Welcome to noise thing. Type " << color("help", 36) << " to get started.\n";
  cout << color("System says: ", 32) << color("Have a wonderful time! ✨ \n\n", 33);

  // Initialize two synths
  FMSynth voice1(440.0, 0.9, samplerate);
  SubSynth voice2(440.0, "tri", samplerate);
  voice1.setModIndex(0.5);

  //assign a function to the JackModule::onProcess
  jack.onProcess = [&voice1, &voice2](jack_default_audio_sample_t *inBuf,
                           jack_default_audio_sample_t *outBuf, jack_nframes_t nframes) {
      for(unsigned int i = 0; i < nframes; i++) {
        outBuf[i] = ((voice1.getSample() + voice2.getSample()) / 2);

        voice1.next();
        voice2.next();
      }
      return 0;
  };

  jack.autoConnect();

  // Set time variables
  auto previous_time = chrono::high_resolution_clock::now();
  chrono::milliseconds interval(250);

  // Start the TUI loop
  cout << color("> ", 33);
  bool running = true;

  while (running) {
    auto current_time = chrono::high_resolution_clock::now();
    auto elapsed_time = current_time - previous_time;

    // Check if playback is active
    if(playing) {
      // Check if the time is right
      if(elapsed_time > interval) {
        int mel = melodies.size() - 1;
        int len = melodies[mel].getLength();
        // If the full melody has been played...
        if(melody_new_note >= len) {
          // Go back to normal!
          playing = false;
          melody_new_note = 0;

          cout << "|| Melody is over!\n";
          cout << color("> ", 33);
        } else {
          // Get the next note from the melody array
          int note = melodies[mel].shift(melody_new_note);
          // Send it to the synthesizer;
          voice1.play(note);
          voice2.play(note + 7);
          cout << note << " ";
          // Increment the melody index
          melody_new_note++;

          previous_time = current_time;
        }
      }
    } else {
      string command;
      getline(cin, command);

      // Prevent empty lines from printing and causing chaos
      if (!command.empty()) {
        // Handle escape route
        if (command == "exit") {
          cout << color("System says: ", 32) << "Shutting down now. Be safe, friend." << color(" Peace out!", 33) << " ✌️" << endl;
          jack.end();
          running = false;
        }
        // Handle melody generation
        else if (command == "melody generate") {
          cout << "Okay, making melody. What length?\n" << color("> ", 34);

          int len;
          string intermediate;
          getline(cin, intermediate);
          len = stoi(intermediate);

          melodies.emplace_back(len);

          cout << "Done! Type " << color("melody play", 36) << " to play it." << endl;
        }
          // Handle melody playback
        else if (command == "melody play") {
          if (!melodies.empty()) {
            playing = true;
          } else {
            cout << "Whoops! There is no melody to play. Type " << color("melody generate", 36) << " to generate one."
                 << endl;
          }
        }
        // Handle soloing
        else if(command == "solo 1") {
          voice2.setAmplitude(0.0);
          voice1.setAmplitude(0.6);
        }
        else if(command == "solo 2") {
          voice1.setAmplitude(0.0);
          voice2.setAmplitude(0.6);
        }
        // Handle unsolo
        else if(command == "solo reset") {
          voice1.setAmplitude(0.3);
          voice2.setAmplitude(0.3);
        }
        // Handle human player
        else if (command == "play") {
          cout << "Type the note you want to play and hit enter. Type " << color("stop", 36) << " to go back." << endl;

          string note;
          bool human_playing = true;

          // Enter human playing loop
          while (human_playing) {
            // Read note input into string
            cin >> note;

            // Handle stop command
            if (note == "stop") {
              human_playing = false;
            }
            // Handle note input
            else if (!note.empty() && isInteger(note)) {
              // Convert input to int (not reading int immediately because string commands)
              int n = stoi(note);
              if (0 < n && n < 127) {
                voice1.play(n);
                voice2.play(n + 7);
              }
            }
          }
        }
          // Handle scream for help
        else if (command == "help") {
          cout <<
               color("play", 35) << "        play noise thing using keyboard commands" << endl <<
               color("melody", 35) << "      " << color("generate", 35) << " and " << color("play", 35) << " melodies" << endl <<
               color("solo", 35) << "        " << color("[voice number]", 35) << " to solo a voice, " << color("reset", 35) << " to reset all" << endl <<
               color("exit", 35) << "        exit the program" << endl;
        }
          // Handle unknown input
        else {
          cout << "Whoops! " << color(command, 31) << " is not a valid command. Type " << color("help", 36)
               << " for a list of commands." << endl;
        }

        if(command != "exit" && !playing) {
          cout << color("> ", 33);
        }
      }
    }
  }
}
