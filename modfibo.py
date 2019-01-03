#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2015, Ekevoo.com.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
"""

Modulo Fibonacci
================

Usage: ``python modfibo.py [BASE]``
E.g.:  ``python modfibo.py 16``

So you know the Fibonacci sequence, right? It's 1 1 2 3 5 8 13 21 34 55 and so on. After going on the sequence for a
while, I noticed that the least significant digit is a pretty long sequence that should eventually start repeating, but
it was taking way too long. So I started analyzing that particular angle of the sequence (modulo 10); yes, on paper. For
some strange reason I had so much fun with it that I started doing it for other bases: hex, oct, 7, 6, 5… And when I got
home I wrote this little test app to explore bigger bases. Base 11 was really hard to do on paper.

There is no purpose to this. It's just fun with numbers. Either you get it or you're not a nerd, and either way is fine.

"""
import collections
import collections.abc
import itertools
import math
import sys
from typing import Iterable, Dict, List, Sequence, Tuple

import colorama


class Alphabet:
    # 82-symbol base alphabet so that 2-digit representations will use 0-9 at minimum
    ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&?!|/*^+=~-_;:,.'

    def __init__(self, base: int):
        colorama.init()
        self.length = math.ceil(math.log(base, len(self.ALPHABET)))
        symbols = sub_alphabet = self.ALPHABET[:math.ceil(base ** (1 / self.length))]
        # increment the length of each symbol until we reach the target length
        for _ in range(1, self.length):
            symbols = [ii + i for ii in symbols for i in sub_alphabet]
        self.symbols: Sequence[str] = symbols[:base]

    def dump(self, runs: Iterable[List[int]]) -> None:
        for run in runs:
            output = [colorama.Style.BRIGHT, colorama.Fore.MAGENTA, self.symbols[run[-1]]]
            if self.length == 1:
                output.append(colorama.Fore.GREEN)
                output.extend(self.symbols[i] for i in run)
            else:
                zebra = (colorama.Fore.GREEN, colorama.Fore.YELLOW)
                output.extend(i
                              for color, item in zip(itertools.cycle(zebra), run)
                              for i in (color, self.symbols[item]))
            output.append(colorama.Style.RESET_ALL)
            print(''.join(output))


class VisitedMap:
    def __init__(self, side: int):
        self.side = abs(side)
        self.map = 0  # A very large bitmap

    def __call__(self, n1: int, n2: int) -> bool:
        pos = n1 * self.side + n2
        mask = 1 << pos
        try:
            return bool(self.map & mask)
        finally:
            self.map |= mask

    def iterate_free_pairs(self) -> Iterable[Tuple[int, int]]:
        mask = (1 << self.side * self.side) - 1
        pos = 0
        search = mask ^ self.map
        while search:
            while not search & 1:
                search >>= 1
                pos += 1
            yield pos // self.side, pos % self.side
            # Assume the map changed, so reload the search bitmap
            search = (mask ^ self.map) >> pos


def modulo_fibonacci(base: int) -> Iterable[List[int]]:
    """ Generates all Modulo Fibonacci runs """
    if base <= 0:
        raise ValueError('Mod must be positive.')
    visited_map = VisitedMap(base)
    for n1, n2 in visited_map.iterate_free_pairs():
        run = []
        while not visited_map(n1, n2):
            n1, n2 = n2, (n1 + n2) % base
            run.append(n1)
        yield run


def group_by_length(seq: Iterable[list]) -> Dict[int, List[list]]:
    grouped = collections.defaultdict(list)
    for item in seq:
        grouped[len(item)].append(item)
    # Assuming python 3.7 where all dicts are sorted by insertion order
    return {k: v for k, v in sorted(grouped.items(), reverse=True)}


def main():
    try:
        base = int(sys.argv[-1])
    except ValueError:
        base = 10
    if base <= 0:
        print("Base must be positive.")
        return

    # Calculate and dump runs
    grouped_runs = group_by_length(modulo_fibonacci(base))
    Alphabet(base).dump(run for group in grouped_runs.values() for run in group)

    # Report some stats
    histogram = {k: len(v) for k, v in grouped_runs.items()}
    print(f'{sum(histogram.values())} sequences.')
    print('; '.join((f'{a} of {l}' for (l, a) in histogram.items())))


if __name__ == '__main__':
    main()
