#!/usr/bin/env python3

import collections
from charfinder2 import read_index

vocabulary = set()

def load_vocabulary():
    with open('/usr/share/dict/words') as fp:
        for word in fp:
            vocabulary.add(word.strip().upper())


def word_count():
    word_idx, char_idx = read_index()
    counts = [(len(word_idx[word]), word) for word in word_idx if word in vocabulary]
    for count, word in sorted(counts, reverse=True):
        print('{:4d}\t{}'.format(count, word))


if __name__ == '__main__':
    load_vocabulary()
    word_count()
