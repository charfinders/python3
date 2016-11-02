#!/usr/bin/env python3

import pathlib
from urllib import request

UCD_URL = 'http://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt'
UCD_NAME = pathlib.Path(UCD_URL).name


def get_ucd_lines():
    if pathlib.Path(UCD_NAME).exists():
        with open(UCD_NAME, 'rt', encoding='ascii') as fp_in:
            text = fp_in.read()
    else:
        print('downloading {}...'.format(UCD_NAME))
        with request.urlopen(UCD_URL) as fp_in:
            text = fp_in.read().decode('ascii')
        with open(UCD_NAME, 'wt', encoding='ascii') as fp_out:
            fp_out.write(text)

    return text.strip().split('\n')


def search(lines, words):
    words = {word.upper() for word in words}
    if not words:
        return
    for line in lines:
        codepoint, name, *rest = line.split(';')
        if name.startswith('<'):
            continue
        name_set = set(name.replace('-', ' ').split())
        if words <= name_set:
            print(chr(int(codepoint, 16)), name)


if __name__ == '__main__':
    
    import sys

    if len(sys.argv) > 1:
        search(get_ucd_lines(), sys.argv[1:])
    else:
        print('usage: {} <word1> <word2> ...'.format(sys.argv[0]))
