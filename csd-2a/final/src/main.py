import playback, ui, algorithm, train
import multiprocessing
import midiutil
import mido

# Start by training the model
# Note that this only trains a model when no previous model is found.
algorithm.train()
# Use the previously trained model to generate a rhythm
rhythm = algorithm.gen((5, 4), 16, 4)

# Convert the generated rhythm to timestamps
# playback.extract()
# playback.play()

# ui_proc = multiprocessing.Process(ui.gather_input)


def handle_input(command):
    print(command)
    if command == "play":
        playback.play()
    elif command == "help":
        print('Help options include:')


while True:
    cmd = input("Command: ")
    handle_input(cmd)
