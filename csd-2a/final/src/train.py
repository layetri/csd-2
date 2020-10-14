import mido
import os
import collections
import pickle
import errno
from termcolor import colored

# Define the master timeline, on which a count of all events per timestamp is stored
master_timeline = {}
quantize = 8


# Converts the global master timeline from amounts to percentages
def convert_to_perc(total):
    for time in master_timeline:
        for note in master_timeline[time]:
            master_timeline[time][note] = master_timeline[time][note] / total


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
def train(signature, series="user"):
    # Define the base variables
    file_count = 0
    directory = str(signature[0])+"-"+str(signature[1])

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
            scale = 48 / mid.ticks_per_beat

            # Define the per-file timeline and timekeeper
            timeline = {}
            timekeeper = 0

            # Iterate over all MIDI tracks
            for i, track in enumerate(mid.tracks):
                # Skip the first track as it only contains metadata
                if i > 0:
                    # For each note in the track
                    for msg in track:
                        # Increment the timekeeper by the MIDI message's time delta
                        timekeeper += round(msg.time * scale)
                        if msg.type == 'note_on':
                            print(msg, "time-delta =", round(msg.time * scale), 'timekeeper =', timekeeper, 'rounded =', round(timekeeper / quantize) * quantize)
                        # Quantize the timekeeper to avoid confusion from possible swing in the source files
                        timekeeper = round(timekeeper / quantize) * quantize

                        # Filter out note_off messages
                        if msg.type == 'note_on' and msg.velocity > 0:
                            # Append to the local timeline
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
            print(timeline)
            print(colored('√', 'green'), "Done. Moving to next file...\n")
        else:
            # The file was not a MIDI file, so we move on.
            print(colored('×', 'red'), colored(filename, 'yellow'), "is not a MIDI file. Skipping...\n")

    # Inform the user that training is complete.
    print(colored('√', 'green'), "Training complete.")
    print("Results:", master_timeline)

    # Convert the count results to percentages.
    convert_to_perc(file_count)

    # Define a model file path...
    path = os.path.abspath("../model/"+series+"/"+directory+"/overview.pickle")
    # ...and write the model contents to the file.
    write_data(master_timeline, path)


def model_to_midi(model):
    data = pickle.load(open('../model/'+model+'/overview.pickle', 'rb'))
    sort = collections.OrderedDict(sorted(data.items()))
    print(sort)

    mid = mido.MidiFile(ticks_per_beat=48)
    track = mido.MidiTrack()
    mid.tracks.append(track)
    track.append(mido.MetaMessage('time_signature', numerator=3, denominator=4))
    prev_time = 0

    for time in sort:
        for note in sort[time]:
            t = time - prev_time
            print(t)

            track.append(mido.Message('note_on', note=note, velocity=64, time=t))
            track.append(mido.Message('note_off', note=note, velocity=0, time=0))

            prev_time = time

    mid.save("../dumps/"+model.replace('/', '_')+".mid")


train((3, 4), "example")
model_to_midi('example/3-4')
