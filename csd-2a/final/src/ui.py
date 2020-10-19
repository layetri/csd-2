import playback, ui, algorithm, train
from termcolor import colored
import math
import os

generated = {}
sig = (4, 4)
bpm = 120
division = 16


# Ask the user for a time signature
def time_sig_input():
    global sig
    sig = (4, 4)
    sig_set = None

    print('What', colored('time signature', 'yellow'), 'do you want to use? (Default is ' + str(sig[0]) + '/' + str(sig[1]) + ')')

    while type(sig_set) is not tuple:
        sig_set = input(' => ')
        if not sig_set:
            sig_set = sig
            print(colored('\u221A', 'green'), 'Using default time signature')
        else:
            try:
                # Parse the time signature to a tuple
                sig_set = sig_set.split('/', 2)
                sig_set = (int(sig_set[0]), int(sig_set[1]))

                # Make sure that the denomination has a valid value
                if not math.log2(sig_set[1]).is_integer():
                    raise AssertionError
            except ValueError:
                sig_set = None
                print(colored('\u00D7', 'red'), "Error: could not parse input to tuple. Try again.")
            except AssertionError:
                sig_set = None
                print(colored('\u00D7', 'red'), "Error: not a valid denomination. Try again.")

    if sig_set and sig_set is not sig:
        sig = sig_set


# Ask the user to pick a dataset
def series_input(context):
    # Ask the user to pick a dataset
    series = "example"
    series_set = None

    print('What', colored('dataset', 'yellow'), 'do you want to use? (Default is "example")')

    while type(series_set) is not str:
        series_set = input(' => ')

        if not series_set:
            series_set = series
            print(colored('\u221A', 'green'), 'Using default dataset')

        # Check if the series directory exists for the desired action
        if not os.path.isdir('../' + context + '/' + series_set + '/' + str(sig[0]) + '-' + str(sig[1])):
            series_set = None
            print(colored('\u00D7', 'red'), "Error: model not found. Try again.")

    if series_set is not series:
        series = series_set

    return series


# Ask the user for the division
def division_input():
    global division
    division_set = None

    print('What', colored('subdivision', 'yellow'), 'do you want to use? (Default is', str(division) + 'th notes)')

    while type(division_set) is not int:
        division_set = input(' => ')
        if not division_set:
            division_set = division
            print(colored('\u221A', 'green'), 'Using default subdivision')
        else:
            try:
                # Parse the division to a number
                division_set = int(division_set)

                # Make sure that the division has a valid value
                if not math.log2(division_set).is_integer():
                    raise AssertionError
            except ValueError:
                division_set = None
                print(colored('\u00D7', 'red'), "Error: could not parse input to number. Try again.")
            except AssertionError:
                division_set = None
                print(colored('\u00D7', 'red'), "Error: not a valid subdivision. Try again.")

    if division_set is not division:
        division = division_set


# Ask the user for the length
def length_input():
    length = 4
    length_set = None

    print('What should the', colored('length', 'yellow'), 'of the rhythm be? (Default is 4 measures)')

    while type(length_set) is not int:
        length_set = input(' => ')
        if not length_set:
            length_set = length
            print(colored('\u221A', 'green'), 'Using default length')
        else:
            try:
                # Parse the length to a number
                length_set = int(length_set)
            except ValueError:
                length_set = None
                print(colored('\u00D7', 'red'), "Error: could not parse input to number. Try again.")

    if length_set is not length:
        length = length_set

    return length


# Ask the user to pick an evolve option
def evolve_input():
    evolve = False
    evolve_set = None

    print('Should the generated rhythm', colored('evolve', 'yellow') + '? (Default is No)')

    while type(evolve_set) is not bool:
        evolve_set = input(' => ')

        # Parse the value to a bool and assert it is valid
        if not evolve_set:
            evolve_set = evolve
            print(colored('\u221A', 'green'), 'Using default setting for evolve')
        elif evolve_set == "yes":
            evolve_set = True
        elif evolve_set == "no":
            evolve_set = False
        else:
            evolve_set = None
            print(colored('\u00D7', 'red'), "Error: input is neither \"yes\" or \"no\". Try again.")

    if evolve_set is not evolve:
        evolve = evolve_set

    return evolve


def do_train():
    print(colored('Initializing training...', 'cyan'))

    # Ask the user for a time signature
    time_sig_input()
    # Ask the user for a dataset to use
    series = series_input('train')

    # Start the training
    print(colored('\nStarting training...', 'cyan'))
    train.train(sig, series)


def do_generate():
    global generated

    print(colored('Initializing rhythm generation...', 'cyan'))
    # Ask the user for a time signature
    time_sig_input()

    # Ask the user for the division
    division_input()

    # Ask the user for the length
    length = length_input()

    # Ask the user to pick a dataset
    series = series_input('model')

    # Ask the user to pick an evolve option
    evolve = evolve_input()

    # Generate a rhythm with the user input and store it
    generated = algorithm.gen(sig, division, length, series, evolve)


def do_play():
    try:
        playback.init(generated)
    except ValueError:
        print(colored('\u00D7', 'red'), 'Error: no rhythm was found. Please run', colored('generate', 'yellow'),
              'and try again.')


def do_export():
    print('Wanna export?')


def handle_input(command):
    if command == "play":
        # Guide the user to play back the generated rhythm
        do_play()
    elif command == "train":
        # Guide the user to train a model
        do_train()
    elif command == 'generate':
        # Guide the user to generate a new rhythm
        do_generate()
    elif command == 'export':
        do_export()
    elif command == 'exit':
        print('Thank you for using', colored('NeuroBeat', 'cyan') + '. Bye bye!')
        exit()
    elif command == 'about':
        packages = ['mido', 'termcolor', 'pygame']

        print(colored('NeuroBeat', 'cyan'), 'was built by Dani\u00EBl Kamp. Copyright \u00A9 2020.')
        print('NeuroBeat depends on the following packages:')

        for package in packages:
            print('-', package)
    elif command == "help":
        # Print the help page
        print('The following commands are available for you to use:')
        print(colored('train', 'cyan'), '        Train a model for a specified dataset.')
        print(colored('generate', 'cyan'), '     Generate a rhythm using a specified model.')
        print(colored('play', 'cyan'), '         Play back the generated rhythm.')
        print(colored('export', 'cyan'), '       Write the generated rhythm to a MIDI file.')
        print(colored('about', 'cyan'), '        Display info about the program.')
        print(colored('exit', 'cyan'), '         Quit the program.')
    else:
        # Handle unknown commands
        print('Unknown command. Type', colored('help', 'yellow'), 'for a list of included commands.')

    # Print a blank line after finishing
    print('')
