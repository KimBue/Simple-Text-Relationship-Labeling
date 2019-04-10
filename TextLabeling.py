"""
Main script
author: Kim Bürgl
"""
from view import *
import math
import nltk
class LabelTexts:
    """
    Inputfile is the path to a File with one Document per Line
    inputindexes is  the path to a file with relations of documentindexes to be labeled. Each line is in format "X Y" with X and Y as indexes of documents
        Indexes in this file are expected to augment, which makes parsing faster ( example: (0 2) (0 4) (1 3) (1 7) (2 1) (2 7), eacht tupel as a line in the file
    outputfilename is the name of the file created in this format per line: "X Y Z" where  X and why are indexes and Z is the label  given  by
    labels,  the path to  a file with each line another label, format as following: "k label" with k as a number and label as a string
    """
    def __init__(self, inputfile, inputindexes, outputfilename, labels, nbOfPairsPerDoc = -1, docSize = math.inf, metaDataFile = None):
        self.inputfile = inputfile
        self.inputindexes = inputindexes
        self.outputfilename = outputfilename
        self.initLabels(labels)
        self.leftFileReader = FileIterator(self.inputfile)
        self.rightFileReader = FileIterator(self.inputfile)
        self.nbOfPairsPerDoc = nbOfPairsPerDoc
        self.lastLeftIndex = -1
        self.docSize = docSize
        if metaDataFile is not None:
            self.left_metadata = FileIterator(metaDataFile)
            self.right_metaData = FileIterator(metaDataFile)
        else:
            self.left_metadata = None
            self.right_metaData = None



    def limitSameDocument(self, index):
        """
        If there is a nbOfPairsPerDoc set, this function returns True if the limit is reached
        :param index: current left index value
        :return: this function returns True if the limit is reached
        """
        if index == self.lastLeftIndex:
            self.countSameDocs += 1
        else:
            self.countSameDocs = 0
        self.lastLeftIndex = index
        if self.countSameDocs >= self.nbOfPairsPerDoc:
            return True
        else:
            return False

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
            if self.nbOfPairsPerDoc != -1 and self.limitSameDocument(index[0]):
                #reverse counter, because not presented candidates should not be part of the documnt limit
                counter -= 1
                continue
            fileA, fileB = self.leftFileReader.getLine(int(index[0])), self.rightFileReader.getLine(int(index[1]))
            if self.isTokenLengthLimit(fileA, fileB):
                continue
            self.label(fileA, fileB, int(index[0]), (int(index[1])))
            print("Candidate Number " + str(counter) +" labeled. Next one...")

    def label(self, textA, textB, indexA, indexB):
        if self.left_metadata is not None and self.right_metaData is not None:
            print_metadata(self.left_metadata.getLine(indexA), self.right_metaData.getLine(indexB), 100)
        printTexts(textA, textB, 100)
        label = printLabelQuestion(self.labels)
        self.writeToFile(indexA, indexB, label)

    def writeToFile(self, indexA, indexB, label):
        f = open(self.outputfilename, 'a')
        f.write(str(indexA) + " " + str(indexB) + " " + str(label) + "\n")
        f.close()

    def isTokenLengthLimit(self,textA, textB):
        tokensA = nltk.word_tokenize(textA)
        tokensB = nltk.word_tokenize(textB)
        if len(tokensA)> self.docSize or len(tokensB) > self.docSize:
            return True
        else:
            return False




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
    labelTexts = LabelTexts("examples/inputfile", "examples/candidate_indexes", "examples/out", "examples/labels", docSize=15000)
    labelTexts.start(1)



    