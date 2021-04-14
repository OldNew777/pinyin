from Markov import Markov
import json
import math
import sys

def train():
    global markov

    print('start loading files')

    markov.load('sina_news_gbk', 'gbk')
    markov.load('novels', 'utf-8')
    markov.load('test_txt', 'utf-8')

    print('start calculating')

    markov.train()
    return

if __name__ == '__main__':
    lambda0 = 0
    if len(sys.argv) == 2:
        lambda0 = float(sys.argv[1])
    markov = Markov(lambda0)
    print('lambda = {0}'.format(lambda0))
    train()

    print('start saving')
    # save the 'first' list
    with open('../data/first.json', 'w', encoding='utf-8') as outputfile:
        json.dump(markov.first, outputfile, indent = 4)

    # save the transitionMatrix
    # separate the list into several parts to save
    for number in range((markov.sizeCharacters // 300) + 1):
        with open('../data/transitionMatrix' + str(number) + '.json', 'w', encoding='utf-8') as outputfile:
            tmp_list = markov.transition[number * 300 : min((number + 1) * 300, markov.sizeCharacters)]
            json.dump(tmp_list, outputfile, indent = 4)
