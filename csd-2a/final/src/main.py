import ui
from termcolor import colored

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Example Usage:
# Train a model on a specified dataset
# => train.train((6, 8), 'example')
# Use the previously trained model to generate a rhythm
# => rhythm = algorithm.gen((6, 8), 16, 4)
# Play back the generated rhythm
# => playback.play()

print('Welcome to', colored('NeuroBeat', 'cyan') + '!')
print('Type', colored('help', 'yellow'), 'for a list of possible commands.\n')

while True:
    cmd = input("Command: ")
    ui.handle_input(cmd)
