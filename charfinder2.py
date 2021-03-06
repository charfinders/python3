#!/usr/bin/env python3

"""
charfinder2.py:
    Searches for Unicode characters named with the words given.
    Builds inverted index of UCD (Unicode Character Database).
"""

import pathlib
from urllib import request
import collections
import functools
import operator
import pickle

UCD_URL = 'http://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt'
UCD_NAME = pathlib.Path(UCD_URL).name
INDEX_NAME = 'charfinder_index.pickle'


def download_ucd():
    print('downloading {}...'.format(UCD_NAME))
    with request.urlopen(UCD_URL) as fp_in:
        text = fp_in.read().decode('ascii')
    with open(UCD_NAME, 'wt', encoding='ascii') as fp_out:
        fp_out.write(text)
    return text


def read_ucd():
    if pathlib.Path(UCD_NAME).exists():
        with open(UCD_NAME, 'rt', encoding='ascii') as fp_in:
            text = fp_in.read()
    else:
        text = download_ucd()

    return (line for line in text.split('\n') 
                 if line.strip() and not line.startswith('#'))


def parse(ucd_line):
    parts = ucd_line.split(';')
    char = chr(int(parts[0], 16))
    name = parts[1]
    name_set = set(name.replace('-', ' ').split())
    if parts[10]:
        old_name = parts[10]
        old_name_set = set(old_name.replace('-', ' ').split())
        if old_name_set - name_set:
            name += ' | ' + old_name
            name_set |= old_name_set
    return char, name, name_set


def build_index():
    lines = read_ucd()
    word_idx = collections.defaultdict(set)
    char_idx = {}
    for line in lines:
        char, name, name_set = parse(line)
        if name.startswith('<'):
            continue
        for word in name_set:
            word_idx[word].add(char)
        char_idx[char] = name
    with open(INDEX_NAME, 'wb') as fp:
        pickle.dump((word_idx, char_idx), fp)
    return word_idx, char_idx


def read_index():
    if pathlib.Path(INDEX_NAME).exists():
        with open(INDEX_NAME, 'rb') as fp:
            word_idx, char_idx = pickle.load(fp)
    else:
        word_idx, char_idx = build_index()
    return word_idx, char_idx


def search(word_idx, char_idx, words):
    if not words:
        return
    words = (word.upper() for word in words)
    found = functools.reduce(operator.and_, (word_idx[word] for word in words))
    for char in sorted(found):
        yield char, char_idx[char]


def main():
    import sys

    if len(sys.argv) < 2:
        print('usage: {} <word1> <word2> ...'.format(sys.argv[0]))
        sys.exit()

    for char, name in search(*read_index(), sys.argv[1:]):
        print(char, name)


if __name__ == '__main__':
    main()
