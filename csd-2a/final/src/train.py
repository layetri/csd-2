import mido
import os
import collections

# Define the master timeline, on which a count of all events per timestamp is stored
master_timeline = {}


def train(signature, series="user"):
    directory = str(signature[0])+"-"+str(signature[1])

    for filename in os.listdir('../train/'+directory):
        print("NOW TRAINING ON", filename, "\n")

        mid = mido.MidiFile('../train/'+directory+'/'+filename)
        scale = 48 / mid.ticks_per_beat
        print("PPQ:", mid.ticks_per_beat)

        timeline = {}
        timekeeper = 0

        for i, track in enumerate(mid.tracks):
            if i > 0:
                for msg in track:
                    if msg.type == 'note_on' and msg.velocity > 0:
                        print(msg)
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

                        # Increment the timekeeper by the MIDI message's time delta
                        timekeeper += round(msg.time * scale)
                        # Quantize the timekeeper to avoid confusion from possible swing in the source files
                        timekeeper = round(timekeeper / 4) * 4

        print(timeline, "\n\n=> Done. Next file please... <=\n")


train((3, 4), "example")
ordered = collections.OrderedDict(sorted(master_timeline.items()))
print(ordered)
