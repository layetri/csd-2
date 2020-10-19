import threading
import time
import mido
from termcolor import colored

ppq = 48
bpm = 120
abs_interval = 60 / (bpm * ppq)

loop = False
proc = None
gm_output = None

timeline = {}


# Setter for the playback bpm
def set_bpm(value):
    global bpm, abs_interval
    print(colored('Setting BPM to ' + str(value), 'cyan'))
    if bpm is not value:
        bpm = value
        abs_interval = 60 / (bpm * ppq)


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
        # Open MIDI output
        self.gm_out = mido.open_output(gm_output)

    def run(self):
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
                        # ...stop the thread.
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
        # Set the exit event
        self.exit.set()


# Initialization function for playback mode
def init(rhythm):
    global proc, gm_output, timeline, loop

    # If a rhythm is present
    if bool(rhythm):
        # Store it in the global timeline
        timeline = rhythm
        play_state = True
        playing = False

        # Set the mido backend
        mido.set_backend('mido.backends.rtmidi')

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
                playing = True
                proc.start()

            # Handle "stop" command
            elif cmd == 'stop':
                playing = False
                proc.shutdown()
                proc.join()

                play_state = False
                print(proc)

            # Handle "bpm" command
            elif cmd.split(' ')[0] == 'bpm':
                arr = cmd.split(' ')
                if len(arr) == 2:
                    try:
                        set_bpm(int(arr[1]))
                    except ValueError:
                        print(colored('\u00D7', 'red'), "Error: could not parse argument to number. Try again.")
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

            # Handle "help" command
            elif cmd == 'help':
                print('Here are your playback commands:')

            # Handle unknown command
            else:
                print('Unknown command. Type', colored('help', 'yellow'), 'for a list of included commands.')
    else:
        # If no rhythm is present, an exception is raised
        raise ValueError
