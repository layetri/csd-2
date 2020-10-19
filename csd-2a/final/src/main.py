import ui
from termcolor import colored

# Example Usage:
# Train a model on a specified dataset
# => train.train((6, 8), 'example')
# Use the previously trained model to generate a rhythm
# => rhythm = algorithm.gen((6, 8), 16, 4)
# Provide playback controls for the generated rhythm
# => playback.init(rhythm)

# Welcome the user~ (with tea or something, idk)
print('Welcome to', colored('NeuroBeat', 'cyan') + '!')
print('Type', colored('help', 'yellow'), 'for a list of possible commands.\n')

# Let the party begin!
while True:
    cmd = input("Command: ")
    ui.handle_input(cmd)
