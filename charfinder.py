#!/usr/bin/env python3

"""
charfinder.py:
    Downloads and scans UCD (Unicode Character Database)
    searching for character named with the words given.
"""

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


def parse(ucd_line):
    """
        >>> line = '002E;FULL STOP;Po;0;CS;;;;;N;PERIOD;;;;'
        >>> char, name, name_set = parse(line)
        >>> char, name
        ('.', 'FULL STOP')
        >>> sorted(name_set)
        ['FULL', 'PERIOD', 'STOP']
        >>> line = '005F;LOW LINE;Pc;0;ON;;;;;N;SPACING UNDERSCORE;;;;'
        >>> char, name, name_set = parse(line)
        >>> char, name
        ('_', 'LOW LINE')
        >>> sorted(name_set)
        ['LINE', 'LOW', 'SPACING', 'UNDERSCORE']

    """
    codepoint, name, *rest = ucd_line.split(';')
    name_set = set(name.replace('-', ' ').split())
    old_name = rest[8]
    if old_name:
        name_set |= set(old_name.replace('-', ' ').split())
        name += ' (old: {})'.format(old_name)
    return chr(int(codepoint, 16)), name, name_set


def scan(lines, words):
    if not words:
        return
    words = {word.upper() for word in words}
    for line in lines:
        char, name, name_set = parse(line)
        if name.startswith('<'):
            continue
        if words <= name_set:
            yield char, name


if __name__ == '__main__':

    import sys

    if len(sys.argv) > 1:
        for char, name in scan(read_ucd(), sys.argv[1:]):
            print(char, name)
    else:
        print('usage: {} <word1> <word2> ...'.format(sys.argv[0]))
