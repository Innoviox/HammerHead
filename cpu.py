from player import *

class CPU(Player):
    def __init__(self, root, rack):
        self.root = root
        self.name = "CPU"
        self.extraList = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", \
             "TWS", "DWS", "TLS", "DLS", \
             "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O ", \
             "*", " "]
        self.board = [[" ", "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O "],
            ['01', 'TWS', ' ', ' ', 'DLS', ' ', ' ', ' ', 'TWS', ' ', ' ', ' ', 'DLS', ' ', ' ', 'TWS'],
            ['02', ' ', 'DWS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'DWS', ' '],
            ['03', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' '],
            ['04', 'DLS', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' ', 'DLS'],
            ['05', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' '],
            ['06', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' '],
            ['07', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', ' '],
            ['08', 'TWS', ' ', ' ', 'DLS', ' ', ' ', ' ', 'B', 'O', 'G', ' ', 'DLS', ' ', ' ', 'TWS'],
            ['09', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', ' '],
            ['10', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' '],
            ['11', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' '],
            ['12', 'DLS', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' ', 'DLS'],
            ['13', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' '],
            ['14', ' ', 'DWS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'DWS', ' '],
            ['15', 'TWS', ' ', ' ', 'DLS', ' ', ' ', ' ', 'TWS', ' ', ' ', ' ', 'DLS', ' ', ' ', 'TWS']]        
        self.score = 0
        self.scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
       "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
       "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
       "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
       "x": 8, "z": 10, "?" : 0}
        
        self.scoreList = ['TWS', 'DWS', 'TLS', 'DLS']
        self.rack = rack
        super(CPU, self).drawTiles()
        #OSPD stands for official scrabble player's dictionary
        #taken from http://www.puzzlers.org/pub/wordlists/ospd.txt #/Volumes/PYTHONDISK/
        try:
            ospd = open("newDict.txt").read().split("\n") #taken from https://raw.githubusercontent.com/xjtian/PyScrabble/master/wordlists/OSPD4_stripped.txt
            self.ospd = []
            for word in ospd:
                self.ospd.append(word.strip())
        except:
            popup(self.root, "Dictionary File Not Found", "Dictionary File Not Found\n\n\n", 500, 500)
            end()
        self.turnrotation = 0
    def getAllCorrectCombinations(self, iterable, maxDepth):
        allWords = []
        for depth in range(0, maxDepth + 1):
            for word in permutations(iterable, depth):
                allWords.append("".join(word))

        allWords.pop(0)
        correctWords = []
        for word in allWords:
            if self.checkWord(word):
                correctWords.append(word)

        return correctWords
    
    def checkWord(self, word):
        if len(word) > 1:
            try:
                subdict = open("resources/" + word[:2] + ".txt").read().split()
            except:
                return False
            if word.upper() in subdict:
                return True
            return False
        return False
        
        

    def addKey(self, dictToCheck, key, value):
        super(CPU, self).addKey(dictToCheck, key, value)
        
    def drawTiles(self):
        if len(self.rack) < 7:
            while len(self.rack) < 7 and len(distribution) > 0:
                letter = choice(distribution)
                distribution.remove(letter)
                self.rack.append(letter.upper())
    #Here's some functions that are in the player class but unfortunately could
    #not be supered because they had to be changed slightly
    def checkWholeBoard(self, boardToCheck, isFirstTurn):
        touchingList = []
        for row in range(1, 16):
            for column in range(1, 16):
                attributes = self.getAttributes("%d,%d" % (row, column), boardToCheck)
                if attributes['text'][0] != " " and attributes['text'] not in self.scoreList:
                    touchingList.append(attributes)
        touchingList = self.removeDuplicates(touchingList)
        for item in touchingList:
            if item['numTouchingLetters'] == 0:
                return False, "Must Be Connected2"
        words = self.getBoardWords(boardToCheck)
        #Checking that words are contiguous algorithm is below.
        if isFirstTurn and boardToCheck[8][8][0] != "*":
            pass
        else:
            if isFirstTurn and boardToCheck[8][8][0] == "*":
                return False, "Must Touch Star"
            else:
                if words:
                    for word in words:
                        letters = words[word]
                        totalTouching = 0
                        for letter in letters:
                            totalTouching += letter['numTouchingLetters']

                        if isFirstTurn:
                            minimumTouching = (len(word) * 2) - 2
                        else:
                            minimumTouching = (len(word) * 2) - 1

                        if not(totalTouching >= minimumTouching):
                            return False, "Must Be Connected"
                else:
                    return False
        
        incorrectWords = []
        if words and len(words) < 1:
            return False
        else:
            if words:
                for word in words:
                    if not(self.checkWord(word.lower())):
                        incorrectWords.append(word)
            else:
                return False
            
        if incorrectWords:
            return False, "Invalid Word", incorrectWords
        else:
            return True, words
            
    def getAttributes(self, place, boardToCheck):
        touching = {}
        place = place.split(",")
        row = int(place[0])
        column = int(place[1])
        numTouching = 0
        if not row-1<1:
            try:
                up = boardToCheck[row-1][column]
            except:
                up = "NA"
            touching['up'] = up
            if up.upper() in ascii_uppercase:
                numTouching += 1

        else:
            touching['up'] = 'NA'
            
        if not row+1>15:
            try:
                down = boardToCheck[row+1][column]
            except:
                down = "NA"
            touching['down'] = down
            if down.upper() in ascii_uppercase:
                numTouching += 1

        else:
            touching['down'] = 'NA'

        if not column+1 > 15:
            try:
                right = boardToCheck[row][column+1]
            except:
                right = "NA"
            touching['right'] = right
            if right.upper() in ascii_uppercase:
                numTouching += 1
        else:
            touching['right'] = 'NA'

        if not column-1 < 1:
            try:
                left = boardToCheck[row][column-1]
            except:
                left = "NA"
            touching['left'] = left
            if left.upper() in ascii_uppercase:
                numTouching += 1
        else:
            touching['left'] = 'NA'
            

        touching['numTouchingLetters'] = numTouching
        touching['row'] = row
        touching['column'] = column
        touching['text'] = boardToCheck[row][column]
        return touching
    
    def playAllWords(self, maxlength = None):
        self.rackonv()
        if self.board[8][8] == "*":
            self.isFirstTurn = True
        else:
            self.isFirstTurn = False
            
        print("Loading...This step will take approximately", round(uniform(0.9, 1.2), 4), "seconds.")
        a = time()
        allMoves = []
        allWords = self.removeDuplicates(self.getAllCorrectCombinations(self.rack, 7))
        print("That step actually took", time() - a, "seconds.")
        boards = 0
        possboards = 0
        longwords = []
        if len(allWords) > 0:
            currmaxlen = max(len(i) for i in allWords)
            for word in allWords:
##                if 3 < len(word):
##                    possboards += 344
##                    longwords.append(word)
                if maxlength is None:
                    if len(word) == max(len(i) for i in allWords):
                        possboards += 344
                        longwords.append(word)
                else:
                    if len(word) == maxlength:
                        possboards += 344
                        longwords.append(word)
            
            print("Generating...This step will take approximately", round(possboards * 0.0023, 4), "seconds.")
            a = time()
            for word in longwords:
                    for row in range(1, len(self.board)):
                        for column in range(1, len(self.board[row])):
                            for direction in ["A", "D"]:
                                nbo = self.rNab()
                                if self.placeWord(word, nbo, [row, column], direction):
                                    if self.checkWholeBoard(nbo, self.isFirstTurn)[0]:
                                        qbox = {"word":word, "board":nbo, "place":[row, column], "direction":direction}
                                        allMoves.append(qbox)
                                        self.getScore(qbox)
            print("That step actually took", time() - a, "seconds.")

            return allMoves

        else:
            print("Exchanging...")
            for letter in self.rack:
                self.rack.remove(letter)
            self.drawTiles()
            return "Non"
    def takeTurn(self, maxlen = None):
        plays = self.playAllWords(maxlength = maxlen)
        if plays != "Non":
            self.turnrotation += 1
            self.nondisplay = False
            bestplay = {"score":0}
            for play in plays:
                if play["score"] > bestplay["score"]:
                    bestplay = play
            if bestplay == {"score":0}:
                print("Something went wrong. Reloading...")
                maxleng = max(len(i) for i in self.getAllCorrectCombinations(self.rack, 7))
                self.turnrotation += 1
                if self.turnrotation >= 3:
                    print("Exchanging...")
                    for letter in self.rack:
                        self.rack.remove(letter)
                    self.drawTiles()
                    self.nondisplay = True
                else:
                    self.takeTurn(maxlen = maxleng - 1)
            else:
                self.displayBoard(bestplay["board"])
                print("Word:", bestplay["word"])
                print(self.placonv(bestplay["place"]))
                print("Direction:", self.dirconv(bestplay["direction"]))
                print("Score:", bestplay["score"])
                #self.rackonv()
            if not self.nondisplay and bestplay != {"score":0}:
                self.turnrotation += 1
                self.score += bestplay["score"]
                self.board = bestplay["board"]
                for letter in bestplay["word"]:
                    self.rack.remove(letter)
            
    def dirconv(self, dirinit):
        if dirinit == "A":
            return "Across"
        return "Down"

    def placonv(self, place):
        return "Row: %d\nColumn: %s" % (int(place[0]), ascii_uppercase[int(place[1])-1])

    def rackonv(self):
##        pass
        print("Rack:", end = " ")
        for i in range(len(self.rack)):
            if i != len(self.rack)-1:
                print(self.rack[i], end = ", ")
            else:
                print(self.rack[i])
        #print("\n")
        
    def displayBoard(self, board):
        count = 0
        text = ""
        text += "|"
        for i in range(16):
            line = board[i]
            for j in line:
                if j == " ":
                    if i == 0:
                        j = "  "
                    else:
                        j = "   "
                if j[0] in ascii_uppercase and len(j) < 3:
                    j = " " + j[0] + " "
                text += j
                text += "|"
                count += 1
                if count == 16 and i != 15:
                    text += "\n"
                    text += "-" * 64
                    text += "\n"
                    text += "|"
                    count = 0
        text += "\n"
        print(text)
        
    def placeWord(self, word, board, place, direction): 
        
        start = board[int(place[0])][int(place[1])]
        length = len(word)
        row = int(place[0])
        column = int(place[1])
        score = 0
        for num in range(0, length):

            if direction == 'A':
                try:
                    if board[row][column] not in ascii_uppercase: #checks if space isn't letter
                        if board[row][column] in self.scoreList:
                            pass 
                        board[row][column] = word[num]
                        
                        column += 1
                    else:
                        return False
                except:
                    return False
            else:
                try:
                    if board[row][column] not in ascii_uppercase:
                        board[row][column] = word[num]
                        row += 1
                    else:
                        return False
                except:
                    return False
        return True

    def getBoardWords(self, boardToCheck):
        touchingList = []
        for row in range(1, 16):
            for column in range(1, 16):
                attributes = self.getAttributes("%d,%d" % (row, column), boardToCheck)
                if attributes['text'][0] != " " and attributes['text'] not in self.scoreList:
                    touchingList.append(attributes)
        touchingList = self.removeDuplicates(touchingList)
        for item in touchingList:
            if item['numTouchingLetters'] == 0:
                return False, "Must Be Connected"
        preservedList = []
        for item in touchingList:
            preservedList.append(item)
        words = {}
        touchingListAcross = []
        touchingListDown = []
        for item in touchingList:
            touchingListAcross.append(item)
            touchingListDown.append(item)
        usedLetters = []
        while touchingList:
            wordAcross = ""
            wordStart = touchingList[0]
            column = wordStart['column']
            row = wordStart['row']
            wordLettersAcross = [wordStart]
            wordAcross += wordStart['text'][0]
            while wordStart['right'][0] != " " and wordStart['right'] != "NA":
                right = wordStart['right']
                column += 1
                for item in touchingList:
                    if item['text'] == right and \
                       item['column'] == column and \
                       item['row'] == row and \
                       item in touchingListAcross:
                        touchingListAcross.remove(item)
                        wordStart = item
                        wordAcross += wordStart['text'][0]
                        wordLettersAcross.append(wordStart)
                if wordStart in usedLetters:
                    break
                else:
                    usedLetters.append(wordStart)
            usedLetters = []
            wordDown = ""
            wordStart = touchingList[0]
            column = wordStart['column']
            row = wordStart['row']
            wordLettersDown = [wordStart]
            wordDown += wordStart['text'][0]
            while wordStart['down'][0] != " " and wordStart['down'] != "NA":
                down = wordStart['down']
                row += 1
                for item in touchingList:
                    if item['text'] == down and \
                       item['column'] == column and \
                       item['row'] == row and \
                       item in touchingListDown:
                        touchingListDown.remove(item)
                        wordStart = item
                        wordDown += wordStart['text'][0]
                        wordLettersDown.append(wordStart)
                if wordStart in usedLetters:
                    break
                else:
                    usedLetters.append(wordStart)
            touchingList.remove(touchingList[0])
            if len(wordAcross) > 1:
                words[wordAcross] = wordLettersAcross
            if len(wordDown) > 1:
                words[wordDown] = wordLettersDown

        return words

    def getScore(self, moveAtts):
        row = moveAtts["place"][0]
        column = moveAtts["place"][1]
        specialScores = {"TLS":[], "DLS":[], "DWS":[], "TWS":[]}
        wordsToScore = [moveAtts["word"]]
        for letter in range(len(moveAtts["word"])):
            sp = self.board[row][column]
            if sp == "TWS":
                specialScores["TWS"] = [moveAtts["word"]]
            elif sp == "DWS" or sp == "*":
                specialScores["DWS"] = [moveAtts["word"]]
            elif sp == "TLS":
                specialScores["TLS"].append(moveAtts["word"][letter])
            elif sp == "DLS":
                specialScores["DLS"].append(moveAtts["word"][letter])
            if moveAtts["direction"] == "A":
                spAtts = self.getAttributes("%d,%d" % (row, column), moveAtts["board"])
                if spAtts["up"] in ascii_uppercase:
                    nrow = row
                    word = spAtts["text"]
                    while spAtts["up"] in ascii_uppercase:
                        word += spAtts["up"]
                        if nrow + 1 < 16:
                            nrow += 1
                            spAtts = self.getAttributes("%d,%d" % (nrow, column), moveAtts["board"])
                        else:
                            break
                    if len(word) == 3:
                        word = word[:2]
                    wordsToScore.append(word)
                    
                spAtts = self.getAttributes("%d,%d" % (row, column), moveAtts["board"])
                if spAtts["down"] in ascii_uppercase:
                    nrow = row
                    word = spAtts["text"]
                    while spAtts["down"] in ascii_uppercase:
                        word += spAtts["down"]
                        if nrow + 1 < 16:
                            nrow += 1
                            spAtts = self.getAttributes("%d,%d" % (nrow, column), moveAtts["board"])
                        else:
                            break
                    if len(word) == 3:
                        word = word[:2]
                    wordsToScore.append(word)
                column += 1
            else:
                spAtts = self.getAttributes("%d,%d" % (row, column), moveAtts["board"])
                if spAtts["right"] in ascii_uppercase:
                    ncol = column
                    word = spAtts["text"]
                    while spAtts["right"] in ascii_uppercase:
                        word += spAtts["right"]
                        if ncol + 1 < 16:
                            ncol += 1
                            spAtts = self.getAttributes("%d,%d" % (row, ncol), moveAtts["board"])
                        else:
                            break
                    if len(word) == 3:
                        word = word[:2]
                    wordsToScore.append(word)
                    
                spAtts = self.getAttributes("%d,%d" % (row, column), moveAtts["board"])
                if spAtts["left"] in ascii_uppercase:
                    ncol = column
                    word = spAtts["text"]
                    while spAtts["left"] in ascii_uppercase:
                        word += spAtts["left"]
                        if ncol + 1 < 16:
                            ncol += 1
                            spAtts = self.getAttributes("%d,%d" % (row, ncol), moveAtts["board"])
                        else:
                            break
                    if len(word) == 3:
                        word = word[:2]
                    wordsToScore.append(word)
                row += 1

        wordScore = 0
        for letter in moveAtts["word"]:
            wordScore += self.scores[letter.lower()]

        for item in specialScores.items():
            scoreType = item[0]
            scoreLetters = item[1]
            if scoreType == "DLS":
                if specialScores.get("DWS"):
                    for i in range(2):
                        for letter in scoreLetters:
                            wordScore += self.scores[letter.lower()]
                elif specialScores.get("TWS"):
                    for i in range(3):
                        for letter in scoreLetters:
                            wordScore += self.scores[letter.lower()]
                else:
                    for letter in scoreLetters:
                        wordScore += self.scores[letter.lower()]
            elif scoreType == "TLS":
                if specialScores.get("DWS"):
                    for i in range(2):
                        for count in range(2):
                            for letter in scoreLetters:
                                wordScore += self.scores[letter.lower()]
                else:
                    for count in range(2):
                        for letter in scoreLetters:
                            wordScore += self.scores[letter.lower()]

        for item in specialScores.items(): #Double and Triple Word have to be evaluated last
            scoreType = item[0]
            scoreLetters = item[1]
            if scoreType == "DWS":
                try:
                    if scoreLetters[0] == moveAtts["word"]:
                        wordScore *= 2
                except:
                    pass
            elif scoreType == "TWS":
                try:
                    if scoreLetters[0] == moveAtts["word"]:
                        wordScore *= 3
                except:
                    pass

        for word in wordsToScore:
            if word != moveAtts["word"]:
                for letter in word:
                    wordScore += self.scores[letter.lower()]
        if len(moveAtts["word"]) == 7:
            wordScore += 50
        moveAtts["score"] = wordScore
        

    def rNab(self):
        nbo = []
        for row in self.board:
            nbo.append([])
            for col in row:
                nbo[-1].append(col)
        return nbo