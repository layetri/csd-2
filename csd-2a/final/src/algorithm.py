import pickle
import random

debug_mode = False


def gen(signature, division, length, series="example", evolve=False, swing=False):
    # Generate a rhythm from the trained model
    model = pickle.load(open('../model/'+series+'/'+str(signature[0])+'-'+str(signature[1])+'/sum.pickle', 'rb'))

    # Prepare dependencies for evolving generation
    if evolve:
        # Open the second layer model
        layer = pickle.load(open('../model/'+series+'/'+str(signature[0])+'-'+str(signature[1])+'/overview.pickle', 'rb'))
        # Prepare an averaging dict
        average = {}

    slices = division * signature[0] * length
    single_measure = division * signature[0]

    # Prepare a dict for the result
    result = {}

    # For every slice within the length of the new rhythm
    for i in range(slices):
        # Determine the position within the measure
        pos = i % single_measure
        # if this relative position exists in the model...
        if pos in model:
            # Debug write-out
            if debug_mode:
                print(i, ':', model[pos])

            # Calculate swing if desired
            if swing:
                slc = i + (round(random.random() * 4) - 2)
            else:
                slc = i

            # If the output dict does not have an entry for the current slice yet, create one.
            if i not in result:
                result[slc] = []

            # Switch for evolving vs. static rhythms
            if evolve:
                # If the current slice exists within the layer model
                if i in layer:
                    # Make sure there is a dict to fill...
                    average[i] = {}
                    # ...and fill it!
                    for note in model[pos]:
                        if note in layer[i]:
                            # Roll a dice based on the average between the two layered models
                            if random.random() < (model[pos][note] + layer[i][note]) / 2:
                                # Write the note!
                                result[slc].append(note)
            else:
                # For each note at the current position...
                for note in model[pos]:
                    # ...roll a dice based solely on the single-measure model...
                    if random.random() < model[pos][note]:
                        # ...and write the note!
                        result[slc].append(note)

    # Debug write-out
    if debug_mode:
        print(result)

    # Return the rhythm!
    return result
