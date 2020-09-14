import time as t

# Define universe
sequence = [2, 4, 4, 2, 2]
bpm = 120
playing = True

while playing:
    # Better scheduling that does not fit within assignment requirements :)
    # for i in range(16):
    #     if i in sequence:
    #         print(i)
    #     t.sleep(bpm / 16)

    # Scheduling based on note durations
    for i in sequence:
        print(i)
        dur = (60 / (bpm * 4)) * i
        t.sleep(dur)
