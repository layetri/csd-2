import multiprocessing
import time
import mido
from termcolor import colored

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
def play(q):
    global playing, timekeeper

    mido.set_backend('mido.backends.pygame')

    prev_time = time.time()
    gm_out = mido.open_output(gm_output)

    playing = True

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
                    break
                timekeeper = 0
                continue

            if not q.empty():
                val = q.get(False)
                if val == 'stop':
                    playing = False
                    timekeeper = 0
                    break
                elif val == 'pause':
                    if q.get() == 'play':
                        continue

        time.sleep(0.001)

    gm_out.close()
    return


# Initialization function for playback mode
def init(rhythm):
    global proc, play_state, playing, gm_output, timeline, loop
    q = multiprocessing.Queue()

    if bool(rhythm):
        timeline = rhythm
        play_state = True
        paused = False

        while play_state:
            if playing:
                if paused:
                    cmd = input('['+colored('paused', 'yellow')+'] Playback command: ')
                else:
                    cmd = input('['+colored('playing', 'cyan')+'] Playback command: ')
            else:
                cmd = input('Playback command: ')

            if cmd == 'pause':
                q.put('pause')
                paused = True
            elif cmd == 'play':
                if paused:
                    q.put('play')
                    paused = False
                else:
                    if proc and proc.is_alive():
                        proc.terminate()
                        proc.join()
                        proc.close()
                    proc = multiprocessing.Process(target=play, args=(q, ))
                    proc.start()
            elif cmd == 'stop':
                q.put('stop')
                play_state = False

                proc.terminate()
                proc.join()
                proc.close()
                proc = None
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
        raise ValueError
