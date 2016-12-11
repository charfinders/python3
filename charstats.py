
import collections

char_count = collections.Counter()

with open('UnicodeData.txt', 'rt', encoding='ascii') as fp:
    for lin in fp:
        parts = lin.split(';')
        if parts[1].startswith('<'):
            continue
        for char in parts[1]:
            if char != ' ':
                char_count[char] += 1

for char, count in char_count.most_common():
    print(count, char, sep='\t')
