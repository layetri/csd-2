import ui
from termcolor import colored

# Example Usage:
# Train a model for a specified
# => train.train((6, 8), 'example')
# Use the previously trained model to generate a rhythm
# => rhythm = algorithm.gen((6, 8), 16, 4)

# Convert the generated rhythm to timestamps
# playback.extract()
# playback.play()

print('Welcome to', colored('NeuroBeat', 'cyan') + '!')
print('Type', colored('help', 'yellow'), 'for a list of possible commands.\n')

while True:
    cmd = input("Command: ")
    ui.handle_input(cmd)
