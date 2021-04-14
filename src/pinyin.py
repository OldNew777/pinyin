import sys
from Viterbi import Viterbi


if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit(1)
    inputName = sys.argv[1]
    outputName = sys.argv[2]

    viterbi = Viterbi()

    with open(inputName, 'r') as inputFile:
        sentenceList = inputFile.readlines()
        
    with open(outputName, 'w', encoding='utf-8') as outputFile:
        for sentence in sentenceList:
            sentence = sentence.strip()
            translation = viterbi.translate(sentence)
            outputFile.write(translation)
            outputFile.write('\n')