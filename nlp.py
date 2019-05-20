from nltk.corpus import wordnet

import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
from nltk.corpus import wordnet
import string
import logging
import multiprocessing
import os
import sys
from gensim.models.word2vec import LineSentence
from gensim.models.word2vec import Word2Vec


# stopwords = nltk.corpus.stopwords.words("english")
# stopwords.extend(string.punctuation)
# stopwords.append('')

# def get_wordnet_ps(pos_tag):
#     if pos_tag[1].startsw


def syn_ant(word):
    for syn in wordnet.synsets(word):
        synonyms = []
        antonyms = []
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
        return synonyms


# def useContextToTranslate(curr_line):
#     tokens = curr_line.split(" ")



def execute():
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
    
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("Running %s", ' '.join(sys.argv))
    
    # Check and process input arguments.
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    inp, outp, veco = sys.argv[1:4]

    max_length = 0
    with open(inp, 'r') as f:
        for line in f.readlines():
            max_length = max(max_length, len(line))
    logger.info("Max article length: %s words.", max_length)

    params = {
    'size': 400,
        'window': 10,
        'min_count': 10,
        'workers': max(1, multiprocessing.cpu_count() - 1),
        'sample': 1E-5,
    }

    word2vec = Word2Vec(LineSentence(inp, max_sentence_length=max_length), **params)
    word2vec.save(outp)

    if veco:
        word2vec.wv.save_word2vec_format(outp + '.model.txt', binary=False)


