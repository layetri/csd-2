import mido
import os
import pickle
import errno
import math
import render
from termcolor import colored

# Define the master timeline, on which a count of all events per timestamp is stored
master_timeline = {}
quantize = 8
ppq = 48
signature = None

# Debug Mode toggles various logging functions
debug_mode = False


# Converts the global master timeline from amounts to percentages
def convert_to_perc(total):
    for time in master_timeline:
        for note in master_timeline[time]:
            master_timeline[time][note] = master_timeline[time][note] / total

    if debug_mode:
        print('Weighed results:', master_timeline)


# Merges the master timeline into a single weighed measure
def extract_sum():
    summed = {}
    weight = {}
    ticks_per_measure = ppq * signature[0] / (4 / signature[1])
    length = math.ceil(max(master_timeline) / ticks_per_measure)

    for time in master_timeline:
        # Translate the time stamp to a measure position and quantise it
        new_time = round((time % ticks_per_measure) / 2) * 2
        # Make sure that there is a dict to be filled
        if new_time not in summed:
            summed[new_time] = {}
        # Fill the dict with counts of notes at times
        for note in master_timeline[time]:
            if note in summed[new_time]:
                summed[new_time][note] += master_timeline[time][note]
            else:
                summed[new_time][note] = master_timeline[time][note]

    # Calculate the per-measure averages
    for time in summed:
        weight[time] = {}
        for note in summed[time]:
            weight[time][note] = round((summed[time][note] / length) * 1000) / 1000

    # Debug write-out
    if debug_mode:
        print("Total single measure:", summed)
        print("Average single measure:", weight)

    # Return the generated lists
    return {'summed': summed, 'weighed': weight}


# Writes pickled data to a file on disk
def write_data(data, path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    with open(path, "wb") as f:
        pickle.dump(data, f)


# Trains the model
def train(sig, series="user"):
    global signature
    signature = sig

    # Define the base variables
    file_count = 0
    directory = series+'/'+str(signature[0])+"-"+str(signature[1])

    # For each file in the training directory...
    for filename in os.listdir('../train/'+directory):
        # Check if the file is a MIDI file
        if filename.lower().endswith(('.mid', '.midi')):
            print("Now training on:", colored(filename, 'yellow'))
            # Increase the file counter
            file_count += 1

            # Read the MIDI file
            mid = mido.MidiFile('../train/'+directory+'/'+filename)
            # Calculate a scale factor to scale everything back to 48 PPQ (we don't need a higher resolution)
            scale = ppq / mid.ticks_per_beat

            # Define the per-file timeline and timekeeper
            timeline = {}
            timekeeper = 0

            # Iterate over all MIDI tracks
            for i, track in enumerate(mid.tracks):
                # Only analyze the first track containing note material
                if i < 2:
                    # For each note in the track
                    for msg in track:
                        # Increment the timekeeper by the MIDI message's time delta
                        timekeeper += round(msg.time * scale)

                        # Debug write-out (remove False to enable)
                        if msg.type == 'note_on' and debug_mode:
                            print(msg, "time-delta =", round(msg.time * scale), 'timekeeper =', timekeeper, 'rounded =', round(timekeeper / quantize) * quantize)

                        # Quantize the timekeeper on whole beats to iron out possible humanization in the source files
                        if timekeeper % ppq > ppq - 5 or timekeeper % ppq < 5:
                            timekeeper = round(timekeeper / quantize) * quantize

                        # Filter out note_off messages
                        if msg.type == 'note_on' and msg.velocity > 0:
                            # Append to the local timeline (only when Debug Mode is enabled)
                            if debug_mode:
                                if timekeeper in timeline:
                                    timeline[timekeeper].append(msg.note)
                                else:
                                    timeline[timekeeper] = [msg.note]

                            # Count the global occurrences of the note on the master timeline
                            if timekeeper in master_timeline:
                                if msg.note not in master_timeline[timekeeper]:
                                    master_timeline[timekeeper][msg.note] = 1
                                else:
                                    master_timeline[timekeeper][msg.note] += 1
                            else:
                                master_timeline[timekeeper] = {msg.note: 1}

            # Print the result
            if debug_mode:
                print(timeline)
            print(colored('\u221A', 'green'), "Done. Moving to next file...\n")
        else:
            # The file was not a MIDI file, so we move on.
            print(colored('\u00D7', 'red'), colored(filename, 'yellow'), "is not a MIDI file. Skipping...\n")

    # Inform the user that training is complete.
    print(colored('\u221A', 'green'), "Training complete.")
    if debug_mode:
        print("Results:", master_timeline)

    # Convert the count results to percentages.
    convert_to_perc(file_count)
    single = extract_sum()

    # Define a model file path...
    path = os.path.abspath("../model/"+directory+"/overview.pickle")
    sum_path = os.path.abspath("../model/"+directory+"/sum.pickle")
    # ...and write the model contents to the file.
    write_data(master_timeline, path)
    write_data(single['weighed'], sum_path)

    if debug_mode:
        render.model_to_midi('example/' + str(signature[0]) + '-' + str(signature[1]) + '/overview', signature, ppq)
