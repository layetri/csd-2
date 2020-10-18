import multiprocessing
import time
import mido
from termcolor import colored
import simpleaudio

kick = simpleaudio.WaveObject.from_wave_file('../../../assets/kick.wav')

playing = False
loop = False

ppq = 48
bpm = 120
abs_interval = 60 / (bpm * ppq)
timekeeper = 0

proc = None
play_state = True
gm_output = None

timeline = {}


# Setter for the playback bpm
def set_bpm(value):
    global bpm, abs_interval
    if bpm is not value:
        bpm = value
        abs_interval = 60 / (bpm * ppq)


# Function to be executed in the playback process
def play(e):
    global playing, timekeeper, kick

    mido.set_backend('mido.backends.pygame')

    prev_time = time.time()
    gm_out = mido.open_output(gm_output)

    while playing:
        cur_time = time.time()
        if cur_time - prev_time > abs_interval:
            if timekeeper in timeline:
                for note in timeline[timekeeper]:
                    gm_out.send(mido.Message('note_on', note=note, channel=10))

            prev_time = cur_time
            timekeeper += 1

            if timekeeper > max(timeline):
                if not loop:
                    playing = False
                timekeeper = 0

            if e.is_set():
                playing = False
                timekeeper = 0

        time.sleep(0.001)

    gm_out.close()


# Initialization function for playback mode
def init(rhythm):
    global proc, play_state, playing, gm_output, timeline, loop
    stop_sig = multiprocessing.Event()

    proc = multiprocessing.Process(target=play, args=(stop_sig, ))
    play_state = True

    while play_state:
        if bool(rhythm) or bool(timeline):
            if bool(rhythm):
                timeline = rhythm
            if playing:
                cmd = input('['+colored('playing', 'cyan')+'] Playback command: ')
            else:
                cmd = input('Playback command: ')

            if cmd == 'pause':
                stop_sig.set()
            elif cmd == 'play':
                playing = True
                proc.start()
            elif cmd == 'stop':
                stop_sig.set()
                play_state = False
            elif cmd == 'loop':
                loop = not loop
                print('Loop is now', colored(loop, 'cyan'))
            elif cmd == 'interface':
                outputs = mido.get_output_names()
                print('Available outputs:', outputs)
                output = input('=> Please specify the MIDI interface to use: ')

                if output in outputs:
                    gm_output = output
                else:
                    print(colored('\u00D7', 'red'), 'That interface does not exist.')
            elif cmd == 'help':
                print('Here are your playback commands:')
            else:
                # Handle unknown commands
                print('Unknown command. Type', colored('help', 'yellow'), 'for a list of included commands.')
        else:
            raise AssertionError
