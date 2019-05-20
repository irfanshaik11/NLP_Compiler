from tokenizer import *
import sys
import nlp
import gensim
from gensim.models import Word2Vec


def printToFile(output, filename):
    filename = "/Users/HabibullahShaik/Desktop/Projects/PrinProgFinal/" + filename
    fp = open(filename, "w")
    for item in output:
        print(item, file = fp)

    print("wrote to ", filename)


if __name__ == "__main__":
    if len(sys.argv) <= 1 or len(sys.argv)>4 :
        print("\n       INCORRECT USAGE")
        print("\n       PROPER USAGE IS python3 gps.py inputfilename outputfilename.py")
    else:
        init()

        code, spacing = tokenize(sys.argv[-2])
        # print(code, spacing)
        output = translate(code, spacing)
        numberoftabs = findSpacing(output)
        output = fixIndentation(output, numberoftabs)
        # print(output)


        printToFile(output, sys.argv[-1])
