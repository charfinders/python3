#!/usr/bin/env python3

"""
This script requires Python 3.5 to run.
"""

import asyncio
import aiohttp
import itertools
import sys
import os
import io
import collections
import string


UNICODEDATA_URL = 'http://www.unicode.org/Public/8.0.0/ucd/UnicodeData.txt'


async def spin(msg):
    """Display spinning sequence of ``/-\|``."""
    write, flush = sys.stdout.write, sys.stdout.flush

    for char in itertools.cycle(r'/-\|'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))


async def download(url):
    """Download file from URL, with activity feedback."""
    spinner = asyncio.ensure_future(spin('downloading'))

    resp = await aiohttp.request('GET', url)
    async with resp:
        if resp.status != 200:
            raise aiohttp.HttpProcessingError(
                code=resp.status, message=resp.reason,
                headers=resp.headers)

        text = await resp.text()

    spinner.cancel()
    return text


async def retrieve_data():
    """Read Unicode database, downloading if necessary"""
    _, filename = os.path.split(UNICODEDATA_URL)

    if os.path.exists(filename):
        with open(filename, 'rt', encoding='ascii') as fp:
            ucd_text = fp.read()
    else:
        ucd_text = await download(UNICODEDATA_URL)
        with open(filename, 'wt', encoding='ascii') as fp:
            fp.write(ucd_text)

    return io.StringIO(ucd_text)


def build_indexes(ucd_text):
    """Build codepoint index and name index."""
    code_idx = {}
    name_idx = collections.defaultdict(set)

    for i, line in enumerate(ucd_text):
        code, name, *rest = line.split(';')
        if '<' in name:
            continue  # ignore control characters and ranges
        code_idx[code] = name
        for word in name.split():
            for part in word.split('-'):
                name_idx[part].add(code)
        if len(code_idx) > 100:
            break

    import pprint
    pprint.pprint(code_idx)
    pprint.pprint(name_idx)


async def load_indexes():
    """Load codepoint index and name index."""
    build_indexes(await retrieve_data())


def main():
    loop = asyncio.get_event_loop()
    ucd_text = loop.run_until_complete(load_indexes())

if __name__ == '__main__':
    main()
