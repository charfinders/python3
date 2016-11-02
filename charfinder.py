#!/usr/bin/env python3

import pathlib
from urllib import request

UCD_URL = 'http://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt'
UCD_NAME = pathlib.Path(UCD_URL).name


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

    return text.strip().split('\n')


def parse(line):
    codepoint, name, *rest = line.split(';')
    if name.startswith('<'):
        return '', '', set()
    name_set = set(name.replace('-', ' ').split())
    return chr(int(codepoint, 16)), name, name_set


def scan(lines, words):
    if not words:
        return
    words = {word.upper() for word in words}
    for line in lines:
        char, name, name_set = parse(line)
        if char and words <= name_set:
            yield char, name


if __name__ == '__main__':

    import sys

    if len(sys.argv) > 1:
        for char, name in scan(read_ucd(), sys.argv[1:]):
            print(char, name)
    else:
        print('usage: {} <word1> <word2> ...'.format(sys.argv[0]))
