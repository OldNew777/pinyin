import json
import os
import math

def isChinese(char_in):
    return '\u4e00' <= char_in <= '\u9fff'

def splitChinese(text):
    ans_list = []
    start = -1
    for i in range(len(text)):
        if isChinese(text[i]):
            if start < 0:
                start = i
        else:
            if start < 0:
                continue
            else:
                ans_list.append(text[start:i])
                start = -1

    # end with Chinese character
    if start >= 0:
        ans_list.append(text[start:])

    return ans_list


# ----------------------------------------

class Markov():
    def __init__(self, lambda_in):
        self.sizeCharacters = 6763
        self.lambda0 = lambda_in

        # first read all the Chinese characters
        with open('../data/汉字拼音表/一二级汉字表.txt', 'r', encoding='ansi') as CharacterFile:
            self.Characters = {}
            mainText = CharacterFile.read()
            for i in range(self.sizeCharacters):
                self.Characters[mainText[i]] = i

        # then prepare counting storage
        self.countij = [[0 for i in range(self.sizeCharacters)] for j in range(self.sizeCharacters)]
        self.count = [0 for i in range(self.sizeCharacters)]
        self.first = [0 for i in range(self.sizeCharacters)]
        self.firstAmount = 0
        self.amount = 0
        self.transition = [[0 for i in range(self.sizeCharacters)] for j in range(self.sizeCharacters)]
        # self.Characters[char] = int


    def load(self, foldername, encoding_in):
        # in this function, load input text file and count relevant number data

        path = os.path.join(os.path.dirname(os.getcwd()), foldername)
        filelist = os.listdir(path)

        for filename in filelist:
            print('open ' + filename)
            with open(path + '/' + filename,'r', encoding = encoding_in) as file:
                index = 0
                for piece in file:
                    index += 1
                    print('{0} : intake line -- {1}'.format(filename, str(index)))
                    news = json.loads(piece)

                    title = news['title']
                    main_text = news['html']
                    time = news['time']

                    # get the list of sentences
                    sentence_list = splitChinese(main_text)

                    # process data
                    for sentence in sentence_list:
                        if sentence[0] in self.Characters:
                            # first Character
                            self.firstAmount += 1
                            self.amount += 1
                            self.first[self.Characters[sentence[0]]] += 1

                            self.count[self.Characters[sentence[0]]] += 1
                        for i in range(1, len(sentence)):
                            if sentence[i] not in self.Characters:
                                continue
                            self.amount += 1
                            self.count[self.Characters[sentence[i]]] += 1
                            if sentence[i-1] in self.Characters:
                                self.countij[self.Characters[sentence[i-1]]][self.Characters[sentence[i]]] += 1
        
        return

    def train(self):
        # generate transitionMatrix
        for i in range(self.sizeCharacters):
            for j in range(self.sizeCharacters):
                if self.count[i] == 0:
                    f = self.lambda0 * self.count[j] / self.amount
                else:
                    f = (1 - self.lambda0) * self.countij[i][j] / self.count[i] + self.lambda0 * self.count[j] / self.amount
                if f == 0:
                    self.transition[i][j] = float('-inf')
                else:
                    self.transition[i][j] = math.log(f)
                    
            if self.first[i] == 0:
                self.first[i] = float('-inf')
            else:
                self.first[i] = math.log(self.first[i] / self.firstAmount)
        
        # release the space
        self.count = 0
        self.countij = 0
        return
