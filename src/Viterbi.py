import json
import random

class Viterbi():
    def __init__(self):
        self.sizeCharacters = 6763
        self.sizePinyin = 406
        self.maxHomonyms = 113
        self.Lambda = 0

        # load all the necessary infomation
        self.Characters = {}
        self.PinyinToCharacter = {}
        self.transition = []
        self.first = []

        self.loadCharacters()
        self.loadPinyinToCharacter()
        self.loadFirst()
        self.loadTransitionMatrix()


    # ---------------------------------------------------------
    # load funtion

    def loadCharacters(self):
        # first read all the Chinese characters
        with open('../data/汉字拼音表/一二级汉字表.txt', 'r', encoding='ansi') as CharacterFile:
            self.Characters = {}
            mainText = CharacterFile.read()
            for i in range(self.sizeCharacters):
                self.Characters[mainText[i]] = i
        return

    
    def loadPinyinToCharacter(self):
        # load the links between pinyin and Chinese characters
        with open('../data/汉字拼音表/拼音汉字表.txt', 'r', encoding='ansi') as intputfile:
            self.PinyinToCharacter = {}
            for line in intputfile:
                line = line.strip('\n')
                data = line.split(' ')
                self.PinyinToCharacter[data[0]] = data[1:]
        return

    def loadTransitionMatrix(self):
        self.transition = []
        for number in range((self.sizeCharacters // 300) + 1):
            with open('../data/transitionMatrix' + str(number) + '.json', 'r', encoding='utf-8') as inputfile:
                tmp_list = json.load(inputfile)
                self.transition += tmp_list
        return

    def loadFirst(self):
        with open('../data/first.json', 'r', encoding='utf-8') as intputfile:
            self.first = json.load(intputfile)
        return

    # load funtion
    # ---------------------------------------------------------

    

    def setLambda(self, lambda_in):
        self.Lambda = lambda_in
        return

    def translate(self, sentence):
        # format
        # {'char' : '我', 'P' : -10.4432132134}
        sentence = sentence.lower()
        pinyins = sentence.split(' ')

        sentence_notduplicated = []
        for pinyin in pinyins:
            if pinyin != '':
                sentence_notduplicated.append(pinyin)
        sentence = sentence_notduplicated

        ways = [[{} for i in range(self.maxHomonyms)] for j in range(len(pinyins))]

        num = [0 for i in range(len(pinyins))]

        # guess the first one
        num[0] = len(self.PinyinToCharacter[pinyins[0]])
        for i in range(num[0]):
            Chinese = self.PinyinToCharacter[pinyins[0]][i]
            ways[0][i]['char'] = Chinese
            ways[0][i]['P'] = self.first[self.Characters[Chinese]]
            ways[0][i]['last'] = -1

        # calculate the posibility of every posible choice based on the info got before
        # dynamic programming
        for pinyinIndex in range(1, len(pinyins)):
            # pinyin is in processing
            pinyin = pinyins[pinyinIndex]
            num[pinyinIndex] = len(self.PinyinToCharacter[pinyin])

            for i in range(num[pinyinIndex]):
                # Chinese is the trying Chinese character
                Chinese = self.PinyinToCharacter[pinyin][i]
                ways[pinyinIndex][i]['char'] = Chinese
                ways[pinyinIndex][i]['P'] = float('-inf')
                ways[pinyinIndex][i]['last'] = -1

                for j in range(num[pinyinIndex - 1]):
                    newP = ways[pinyinIndex - 1][j]['P'] + self.transition[self.Characters[ways[pinyinIndex - 1][j]['char']]][self.Characters[Chinese]]
                    if ways[pinyinIndex][i]['P'] < newP:
                        ways[pinyinIndex][i]['P'] = newP
                        ways[pinyinIndex][i]['last'] = j

        # when finish the dynamic programming, choose the best match
        maxP = float('-inf')
        index = -1
        # choose the best match
        for i in range(num[len(pinyins) - 1]):
            if maxP < ways[len(pinyins) - 1][i]['P']:
                maxP = ways[len(pinyins) - 1][i]['P']
                index = i
        # no reasonable match, randomly choose one
        if index == -1:
            index = random.randint(0, num[len(pinyins) - 1])
            if index == num[len(pinyins) - 1]:
                index = 0
        answer = ''

        for i in range(len(pinyins) - 1, 0, -1):
            answer = '{0}{1}'.format(ways[i][index]['char'], answer)
            index = ways[i][index]['last']
            if index == -1:
                index = random.randint(0, num[i - 1])
                if index == num[i - 1]:
                    index = 0

        answer = '{0}{1}'.format(ways[0][index]['char'], answer)
        return answer