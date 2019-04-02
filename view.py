from nltk.tokenize import WhitespaceTokenizer

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

"""
prints texts in two columns, which makes them comparable easily
"""
def printTexts(textA, textB, columnSize):
    print()
    left = [l for l in getNextLine(textA, columnSize)]
    right = [r for r in getNextLine(textB, columnSize)]
    if len(right )> len(left):
        left, right = right, left
    for l in left:
        if len(right)> 0:
           print("".join(word.ljust(columnSize + 5) for word in (l, right.pop(0))))
        else:
            print(l)

"""
splits text in lines by whitespaces to be shorter than columnSize
"""
def getNextLine(str, columnSize):
    token = WhitespaceTokenizer().tokenize(str)
    while len(token) > 0:
        out = ""
        sizeCounter = columnSize
        while len(token)> 0 and sizeCounter > len(token[0]):
            t = token.pop(0)
            out += t + " "
            sizeCounter -= len(t) +1
        if out == "":
            t = token.pop(0)
            out = t[0:columnSize]
            token.insert(0, t[columnSize:])
        yield out

def printLabelQuestion(labels):
    print(bcolors.OKGREEN + "Which label is appropriate for the relationship between those documents? " + bcolors.ENDC)
    for label in labels:
        print("[ " +str(label) + " ] " + labels[label])
    return labelInput(labels)

def labelInput(labels):
    while(True):
        userInput = input("Please type a correct Label Number")
        if userInput in labels:
            return userInput

if __name__ == '__main__':
    printTexts("Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. ", "Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", 50)