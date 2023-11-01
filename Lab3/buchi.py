import json
from typing import List, Tuple, Dict


def matrix_to_dict(matrix):
    result_dict = {}

    for row in matrix:
        key = tuple(row[:2])
        value = row[2]
        result_dict[key] = value

    return result_dict


def readBuchi(filename):
    with open(filename) as f:
        buchi = json.load(f)
    translateFunc = matrix_to_dict(buchi['translateFunc'])
    buchi['translateFunc'] = translateFunc
    return buchi


def NDCBAtoDCBA(automata):
    startState = automata['startState']
    finalStates = automata['finalStates']
    letters = automata['letters']
    transitionFunc = automata['transitionFunc']

    resStates = []
    resTransF = []
    resFinalStates = []

    if startState in finalStates:
        res_startState = [{startState}, None]
    else:
        res_startState = [{startState}, {startState}]

    W = [res_startState]

    while W:
        P, O = W.pop()
        resStates.append([set(P), set(O)])

        if O is None:
            resFinalStates.append([set(P), set(O)])

        for x in letters:
            nextP = transitionFunc[(tuple(P), x)]
            if O is not None:
                nextO = [state for state in transitionFunc
                         [(tuple(O), x)] if state not in finalStates]
            else:
                O = transitionFunc[(
                    tuple(P), x)] - set(finalStates)

            resTransF.append([set(P), set(O), x, [set(nextP), set(nextO)]])

            if [set(nextP), set(nextO)] not in resStates:
                W.append([set(nextP), set(nextO)])

    return {
        'states': resStates,
        'letters': letters,
        'transitionFunc': resTransF,
        'startState': startState,
        'finalStates': resFinalStates
    }


def main():
    NDCBA = readBuchi('buchi.json')
    DCBA = NDCBAtoDCBA(NDCBA)
    print(DCBA)


if __name__ == "__main__":
    main()
