#!/usr/bin/env python3

"""
charfinder.py:
    Searches for Unicode characters named with the words given.
    Downloads and scans UCD (Unicode Character Database).
"""


import pathlib
from urllib import request

UCD_URL = 'http://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt'
UCD_NAME = pathlib.Path(UCD_URL).name


def parse(ucd_line):
    parts = ucd_line.split(';')
    char = chr(int(parts[0], 16))
    name = parts[1]
    if parts[10]:
        old_name = parts[10]
        old_name_set = set(old_name.replace('-', ' ').split())
        name_set = set(name.replace('-', ' ').split())
        if old_name_set - name_set:
            name += ' | ' + old_name
    return char, name


def match(query_set, name):
    name = set(name.replace('-', ' ').split())
    return query_set <= name


def scan(lines, query):
    query = query.upper().replace('-', ' ')
    query_set = set(query.split())
    if not query_set:
        return
    for line in lines:
        char, name = parse(line)
        if match(query_set, name):    
            yield char, name


def download_ucd():
    print('downloading {}...'.format(UCD_NAME))
    with request.urlopen(UCD_URL) as fp_in:
        octets = fp_in.read()
    with open(UCD_NAME, 'wb') as fp_out:
        fp_out.write(octets)
    return octets.decode('ascii')


def read_ucd():
    if pathlib.Path(UCD_NAME).exists():
        with open(UCD_NAME, 'rt', encoding='ascii') as fp_in:
            text = fp_in.read()
    else:
        text = download_ucd()

    return (line for line in text.split('\n') 
                 if line.strip() and not line.startswith('#'))

def main():
    import sys

    if len(sys.argv) < 2:
        print('usage: {} <word1> <word2> ...'.format(sys.argv[0]))
        sys.exit()

    for char, name in scan(read_ucd(), ' '.join(sys.argv[1:])):
        print(char, name)


if __name__ == '__main__':
    main()
