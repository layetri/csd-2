import simpleaudio as sa
import time as t

# Set up environment
play = None
start = None

# Ask for input
bpm = input("give bpm: ")
times = input("rEpeAT h0W mUcH?? ")
playing = True

# Calculate interval
interval = 60000 / int(bpm)

# Load the wave into a WaveObject
wave = sa.WaveObject.from_wave_file("../../assets/testsample.wav")


def spawn_wave_on_main_thread():
    global play
    global start
    start = t.time()
    # Play the sound
    play = wave.play()


while playing:
    if start is not None and t.time() > int(start) + interval:
        spawn_wave_on_main_thread()

# Done!
print("Song's over")