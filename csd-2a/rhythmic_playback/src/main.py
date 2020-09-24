# Import dependencies
import time
import sys
import os
import simpleaudio as sa
import math

# Define the world
# BPM Setter
bpm = 120
bpm_set = None
# Make sure the BPM is a number
while type(bpm_set) is not int:
    bpm_set = input('BPM (default is ' + str(bpm) + '): ')
    # Try parse to number, retry on fail
    try:
        if bpm_set:
            bpm_set = int(bpm_set)
        else:
            bpm_set = bpm
    except ValueError:
        print("Error: could not parse input to number. Try again.")

if bpm_set and bpm_set is not bpm:
    bpm = bpm_set

# Subdivision Setter
subdivision = 16
subd_set = None
# Make sure the subdivision is a number
while type(subd_set) is not int:
    subd_set = input('Subdivision (as note value, default is ' + str(subdivision) + '): ')
    # Try parse to number, retry on fail
    try:
        if subd_set:
            subd_set = int(subd_set)
            # Check if the input is a power of 2 (aka a valid subdivision)
            if not math.log2(subd_set).is_integer():
                raise AssertionError
        else:
            subd_set = subdivision
    except ValueError:
        print("Error: could not parse input to number. Try again.")
    except AssertionError:
        print("Not a valid subdivision, try again.")

if subd_set and subd_set is not subdivision:
    subdivision = subd_set

# Length Setter
length = 16
len_set = None

while type(len_set) is not int:
    len_set = input('Number of notes (default is ' + str(length) + '): ')
    # Try parse to number, retry on fail
    try:
        if len_set:
            len_set = int(len_set)
        else:
            len_set = length
    except ValueError:
        print("Error: could not parse input to number. Try again.")

if len_set and len_set is not length:
    length = len_set

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
    timeslot = notes[current_beat]

    # Visual feedback
    sys.stdout.write("\r " + str(current_beat) + ': ' + str(timeslot))
    sys.stdout.flush()

    # Filter empty spots
    if timeslot[0] is not 'x':
        for sample in timeslot:
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
print("Note options: [k = kick, s = snare, h = hi-hat, x = empty]")
print("To enter multiple notes, separate them with commas")

for i in range(length):
    user_input = input(f'Notes at {i + 1}: ')

    if user_input is not '':
        arr = user_input.split(', ')
        notes.append(arr)
    else:
        notes.append(['x'])

# Clear the screen
os.system('clear')
# Print the input
print(notes)

# Trigger the first sample before the clock starts
trigger_sample()

while True:
    # Store the current time (instead of calling time() twice, which would result in a slight execution time offset)
    cur_time = time.time()
    # Check time difference against interval
    if cur_time - prev_time >= interval:
        # Call a function that searches and plays a sample for the current timestamp
        trigger_sample()
        # Store the current time
        prev_time = cur_time
        # Pause execution for 1ms to relieve the CPU
        time.sleep(0.001)
