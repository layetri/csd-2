import threading
import time
import mido
import pygame
from termcolor import colored

ppq = 48
bpm = 120
abs_interval = 60 / (bpm * ppq)

playing = False
loop = False
proc = None
proc_has_ended = False

gm_output = None
gm_backend = 'rtmidi'

timeline = {}


# Setter for the playback bpm
def set_bpm(value):
    global bpm, abs_interval
    print(colored('Setting BPM to ' + str(value), 'cyan'))
    if bpm is not value:
        if 0 < value < 250:
            bpm = value
            abs_interval = 60 / (bpm * ppq)
        else:
            raise TypeError


# Playhead thread
class Playhead(threading.Thread):
    # Initialize the thread
    def __init__(self):
        threading.Thread.__init__(self)
        self.exit = threading.Event()

        # Initialize the timekeeper
        self.timekeeper = 0
        # Set a baseline timestamp
        self.prev_time = time.time()
        # Set the mido backend
        mido.set_backend('mido.backends.'+gm_backend)
        # Open MIDI output
        self.gm_out = mido.open_output(gm_output)

    def run(self):
        global proc_has_ended, playing
        while not self.exit.is_set():
            # Store the current time
            # # (instead of calling time() twice, which would result in a slight execution time offset)
            cur_time = time.time()
            # Check time difference against interval
            if cur_time - self.prev_time > abs_interval:
                # If the current timekeeper timestamp is found on the timeline
                if self.timekeeper in timeline:
                    # For each note at timekeeper timestamp
                    for note in timeline[self.timekeeper]:
                        # Send out a MIDI message
                        self.gm_out.send(mido.Message('note_on', note=note, channel=10))

                # Store the current timestamp in cache
                self.prev_time = cur_time
                # Increment the timekeeper
                self.timekeeper += 1

                # If there is no more timeline to play,
                if self.timekeeper > max(timeline):
                    # ...and the loop flag has not been set,
                    if not loop:
                        # ...close the MIDI port,
                        self.gm_out.close()
                        # ...raise the flags,
                        proc_has_ended = True
                        playing = False
                        # ...and stop the thread.
                        self.exit.set()
                    # Else, reset the timekeeper to 0 and loop.
                    else:
                        self.timekeeper = 0
                        continue

            # Sleep shortly to lower CPU usage
            time.sleep(0.001)

    def shutdown(self):
        # Close the MIDI port
        self.gm_out.close()
        # Raise the flag
        playing = False
        # Set the exit event
        self.exit.set()


# Initialization function for playback mode
def init(rhythm):
    global proc, gm_output, gm_backend, timeline, loop, proc_has_ended, playing

    # If a rhythm is present
    if bool(rhythm):
        # Store it in the global timeline
        timeline = rhythm
        play_state = True
        playing = False

        # Initialize the Playhead thread
        proc = Playhead()

        # Loop while the Play command is active
        while play_state:
            if playing:
                cmd = input('[' + colored('playing', 'cyan') + '] Playback command: ')
            else:
                cmd = input('Playback command: ')

            # Handle "play" command
            if cmd == 'play':
                if playing and not proc_has_ended:
                    print(colored('\u00D7', 'red'), "Cannot playback twice at the same time.")
                else:
                    if proc_has_ended:
                        proc.shutdown()
                        proc.join()
                        proc = Playhead()
                        proc_has_ended = False
                    playing = True
                    proc.start()

            # Handle "stop" command
            elif cmd == 'stop':
                if proc.is_alive() or playing:
                    playing = False
                    proc.shutdown()
                    proc.join()

                play_state = False

            # Handle "bpm" command
            elif cmd.split(' ')[0] == 'bpm':
                arr = cmd.split(' ')
                if len(arr) == 2:
                    try:
                        set_bpm(int(arr[1]))
                    except ValueError:
                        print(colored('\u00D7', 'red'), "Error: could not parse argument to number. Try again.")
                    except TypeError:
                        print(colored('\u00D7', 'red'), "Error: invalid value. Try again with a number between 0 and 250.")
                else:
                    print(colored('\u00D7', 'red'), 'BPM expects exactly 1 argument,', str(len(arr) - 1), 'given.')

            # Handle "loop" command
            elif cmd == 'loop':
                loop = not loop
                print('Loop is now', colored(loop, 'cyan'))

            # Handle "interface" command
            elif cmd == 'interface':
                outputs = mido.get_output_names()
                print('Available outputs:', outputs)
                output = input('=> Please specify the MIDI interface to use: ')

                if output in outputs:
                    gm_output = output
                else:
                    print(colored('\u00D7', 'red'), 'That interface does not exist.')

            # Handle "backend" command
            elif cmd == 'backend':
                backends = ['rtmidi', 'pygame']
                print('Available backends:', backends)
                backend = input('=> Please specify the backend to use: ')

                if backend in backends:
                    gm_backend = backend
                else:
                    print(colored('\u00D7', 'red'), 'That backend does not exist.')

            # Handle "help" command
            elif cmd == 'help':
                print('The following commands are available for you to use:')
                print(colored('play', 'cyan'), '         Start playback.')
                print(colored('stop', 'cyan'), '         Stop playback and return to the main program.')
                print(colored('loop', 'cyan'), '         Toggle looping. Currently', str(loop))
                print(colored('bpm', 'cyan'), '          Change the playback BPM. Expects the new BPM as its only argument.')
                print(colored('interface', 'cyan'), '    Select the MIDI interface to use.')
                print(colored('backend', 'cyan'), '      Select the backend for mido to use.')

            # Handle unknown command
            else:
                print('Unknown command. Type', colored('help', 'yellow'), 'for a list of included commands.')
    else:
        # If no rhythm is present, an exception is raised
        raise ValueError
