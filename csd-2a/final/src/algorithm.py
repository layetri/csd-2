import pickle
import random


def gen(signature, division, length, series="example", evolve=False):
    # Generate a rhythm from the trained model
    model = pickle.load(open('../model/'+series+'/'+str(signature[0])+'-'+str(signature[1])+'/sum.pickle', 'rb'))

    # Prepare dependencies for evolving generation
    if evolve:
        layer = pickle.load(open('../model/'+series+'/'+str(signature[0])+'-'+str(signature[1])+'/overview.pickle', 'rb'))
        average = {}

    ppq = 48
    increment = ppq / (division / (32 / signature[1]))
    slices = division * signature[0] * length
    single_measure = division * signature[0]

    # Prepare a dictionary for the result
    result = {}

    for i in range(slices):
        pos = i % single_measure
        if pos in model:
            print(i, ':', model[pos])
            if i not in result:
                result[i] = []

            if evolve:
                if i in layer:
                    average[i] = {}
                    for note in model[pos]:
                        if note in layer[i]:
                            if random.random() < (model[pos][note] + layer[i][note]) / 2:
                                result[i].append(note)
            else:
                for note in model[pos]:
                    if random.random() < model[pos][note]:
                        result[i].append(note)

    print(result)
