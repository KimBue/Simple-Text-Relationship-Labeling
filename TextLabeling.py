"""
Main script
author: Kim Bürgl
"""
from view import *
class LabelTexts:
    """
    Inputfile is the path to a File with one Document per Line
    inputindexes is  the path to a file with relations of documentindexes to be labeled. Each line is in format "X Y" with X and Y as indexes of documents
        Indexes in this file are expected to augment, which makes parsing faster ( example: (0 2) (0 4) (1 3) (1 7) (2 1) (2 7), eacht tupel as a line in the file
    outputfilename is the name of the file created in this format per line: "X Y Z" where  X and why are indexes and Z is the label  given  by
    labels,  the path to  a file with each line another label, format as following: "k label" with k as a number and label as a string
    """
    def __init__(self, inputfile, inputindexes, outputfilename, labels):
        self.inputfile = inputfile
        self.inputindexes = inputindexes
        self.outputfilename = outputfilename
        self.initLabels(labels)
        self.leftFileReader = FileIterator(self.inputfile)
        self.rightFileReader = FileIterator(self.inputfile)

    def initLabels(self, labels):
        self.labels = {}
        f = open(labels, "r")
        for line in f:
            line = line.replace("\n", "")
            splitted = line.split(" ", 1)
            self.labels[splitted[0]] = splitted[1]

    def start(self, startIndex = 0):
        f = open(self.inputindexes, "r")
        counter = -1
        for l in f:
            counter +=1
            if counter < startIndex:
                continue #get to he start line
            index = l.split()
            self.label(int(index[0]), (int(index[1])))

    def label(self, indexA, indexB):
        textA = self.leftFileReader.getLine(indexA)
        textB = self.rightFileReader.getLine(indexB)
        printTexts(textA, textB, 100)
        label = printLabelQuestion(self.labels)
        self.writeToFile(indexA, indexB, label)

    def writeToFile(self, indexA, indexB, label):
        f = open(self.outputfilename, 'a')
        f.write(str(indexA) + " " + str(indexB) + " " + str(label) + "\n")
        f.close()



"""
This Object keeps an Document open to make getting consecutive lines faster
"""
class FileIterator:
    def __init__(self, filename):
        self.filename = filename
        self.openFile()

    def __del__(self):
        self.f.close()

    def openFile(self):
        self.f = open(self.filename, "r")
        self.index = 0
        self.line = self.f.readline()

    def getLine(self, index):
        index = int(index)
        if index < self.index:
            self.f.close()
            self.openFile()
        if index == self.index:
            return self.line
        while index > self.index:
            self.line = self.f.readline()
            self.index += 1
        return self.line




if __name__ == '__main__':
    labelTexts = LabelTexts("examples/inputfile", "examples/candidate_indexes", "examples/out", "examples/labels")
    labelTexts.start()



    