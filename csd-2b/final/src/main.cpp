//
// Noise Thing v1.0
// © 2021 Daniël Kamp
//

// Include libraries
#include <iostream>
#include <string>
#include <thread>
#include <vector>
// Might or might not include curses...
//#include <curses.h>
#include "jack_module.h"

// Include program headers
#include "subsynth.h"
#include "fmsynth.h"
#include "melody.h"

// Use std namespace instead of std-littering our code
using namespace std;

// Abstraction to easily provide a text coloring utility
string color(string text, int color) {
  return "\033[" + to_string(color) + "m" + text + "\033[0m";
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

// Main program loop
int main(int argc, char* argv[]) {
  JackModule jack;
  jack.init(argv[0]);
  int samplerate = jack.getSamplerate();

  // Print the welcome screen ✨
  printLogo();
  cout << color("System says: ", 32) << "Welcome to noise thing. Type " << color("help", 36) << " to get started.\n";
  cout << color("System says: ", 32) << color("Have a wonderful time! ✨ \n\n", 33);

  cout << color("> ", 33);

  // Initialize melody vector
  vector<Melody> melodies;

  // Initialize two synths
  SubSynth voice1(440.0, "square", samplerate);
  //FMSynth voice2(440.0,1.1, samplerate);
  SubSynth voice2(440.0, "sine", samplerate);
  voice1.play(60);
  voice2.play(67);

  //assign a function to the JackModule::onProcess
  jack.onProcess = [&voice1, &voice2](jack_default_audio_sample_t *inBuf,
                           jack_default_audio_sample_t *outBuf, jack_nframes_t nframes) {

      static float amplitude = 0.15;

      for(unsigned int i = 0; i < nframes; i++) {
        outBuf[i] = ((voice1.getSample() + voice2.getSample()) / 2) * amplitude;
        outBuf[i] = 0.0;
      }

      return 0;
  };

  jack.autoConnect();

  // Felt cute, might commit deepnote later idk
  //voice1.deepnote();
  //voice2.deepnote();

  // Start the TUI loop
  bool running = true;
  while (running) {
    string command;

    getline(cin, command);

    if (!command.empty()) {
      if (command == "exit") {
        cout << "haha now we exit." << endl;
        jack.end();
        running = false;
      } else if (command == "voice make") {
        //string waveshape;
        //cout << "Okay, making voice. What shape?\n" << color("> ", 34);
        //getline(cin, waveshape);
        //Synth voice(waveshape, samplerate);

        cout << "This command has been disabled for now.";
      } else if (command == "melody generate") {
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
          //thread mel(melody.play);
        } else {
          cout << "Whoops! There is no melody to play. Type " << color("melody generate", 36) << " to generate one."
               << endl;
        }
      }
        // Handle human player
      else if (command == "play") {
        cout << "Type the note you want to play and hit enter. Type " << color("stop", 36) << " to go back." << endl;

        string note;
        bool playing = true;

        while (playing) {
          cin >> note;

          if (note == "stop") {
            playing = false;
          } else if (!note.empty()) {
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
             color("exit", 35) << "        exit the program" << endl;
      }
        // Handle unknown input
      else {
        cout << "Whoops! " << color(command, 31) << " is not a valid command. Type " << color("help", 36)
             << " for a list of commands." << endl;
      }

      if(command != "exit") {
        cout << color("> ", 33);
      }
    }
  }
}
