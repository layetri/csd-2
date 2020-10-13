from scipy import *

beats = 5
measure = [['kick', 'hat'], ['hat'], ['snare', 'hat'], ['hat'], ['hat']]
options = ['kick', 'snare', 'hat']
weighed = {}
significance = []

for beat in measure:
    significance.append(len(beat) / beats)

    for option in options:
        if option in weighed:
            weighed[option] += beat.count(option)
        else:
            weighed[option] = beat.count(option)

for el in weighed:
    weighed[el] = 1 - (weighed[el] / beats)

print(weighed)
print(significance)
