import pickle
import mido
import os
import errno
import collections
from datetime import datetime


# Check if a folder already exists, else create it
def folder_check(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


# Generate a MIDI file
def make_file(data, sig, ppq):
    # Sort the data by timestamp, ascending
    sort = collections.OrderedDict(sorted(data.items()))

    # Initialize a MidiFile object
    mid = mido.MidiFile(ticks_per_beat=ppq)
    # Create and add a track
    track = mido.MidiTrack()
    mid.tracks.append(track)
    # Add a time signature meta message to the track
    track.append(mido.MetaMessage('time_signature', numerator=sig[0], denominator=sig[1]))

    # Set a cache for time
    prev_time = 0

    # Loop over the sorted data
    for time in sort:
        # For each note in each timestamp
        for note in sort[time]:
            # Calculate the time delta
            t = time - prev_time

            # Write a note on and off message
            track.append(mido.Message('note_on', note=note, velocity=64, time=t))
            track.append(mido.Message('note_off', note=note, velocity=0, time=0))

            # Store the current timestamp in the time cache
            prev_time = time

    # Return the file object
    return mid


# Export a trained model to a MIDI file, for testing purposes (undocumented)
def model_to_midi(model, sig, ppq):
    data = pickle.load(open('../model/'+model+'.pickle', 'rb'))
    mid = make_file(data, sig, ppq)
    mid.save("../dumps/"+model.replace('/', '_')+".mid")


# Export a generated rhythm to a MIDI file
def rhythm_to_midi(rhythm, sig, ppq):
    # Generate a MIDI file
    mid = make_file(rhythm, sig, ppq)

    # Check if the exports folder exists
    folder_check('../exports/')

    # Store the generated MIDI file
    mid.save("../exports/"+datetime.today().strftime('%d_%m_%Y-%H_%M_%S')+".mid")
