# Import dependencies
import time
import sys
import os
import simpleaudio as sa

# Define the world
bpm = int(input('BPM: '))
subdivision = int(input('Subdivision: '))
length = int(input('Number of notes: '))

interval = 60 / bpm / (subdivision / 4)
prev_time = time.time()
current_beat = 0

notes = []
sample_lookup = {
    'k': sa.WaveObject.from_wave_file("../../../assets/kick.wav"),
    's': sa.WaveObject.from_wave_file("../../../assets/snare.wav"),
    'h': sa.WaveObject.from_wave_file("../../../assets/hat.wav")
}


def trigger_sample():
    global current_beat

    # Look up the current note
    sample = notes[current_beat]
    # Visual feedback
    sys.stdout.write("\r " + str(current_beat) + ': ' + str(sample))
    sys.stdout.flush()

    # Filter empty spots
    if sample is not 'x':
        # Look up the sample
        file = sample_lookup[sample]
        # And play it
        file.play()

    # Keep track of position and loop back if necessary
    if current_beat < length - 1:
        current_beat += 1
    else:
        current_beat = 0


# Have the user fill the array
for i in range(length):
    user_input = input(f'Note at {i + 1}: ')

    if user_input is not '':
        notes.append(user_input)
    else:
        notes.append('x')

# Clear the screen
os.system('clear')
# Print the input
print(notes)

# Trigger the first sample before the clock starts
trigger_sample()

while True:
    if time.time() - prev_time >= interval:
        trigger_sample()
        prev_time = time.time()
