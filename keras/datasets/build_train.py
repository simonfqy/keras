from __future__ import absolute_import
import sys
import os


def build_train(dataPath,trainFile):
    #The Path to Train File
    f = open(trainFile,'w')

    for root, dirs, filenames in os.walk(dataPath):
        for filename in filenames:
            print filename
            f.write(filename + os.linesep)

    f.close()
