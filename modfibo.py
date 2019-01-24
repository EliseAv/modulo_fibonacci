#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2015-2019, Ekevoo.com.
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

The Fibonacci sequence https://oeis.org/A000045 is 1 1 2 3 5 8 13 21 34 55 and so on.

It's not hard to conclude that the sequence's least significant digit starts repeating after a while, but I was doing
it on paper, and it was taking way too long. For some strange reason I had so much fun doing it manually, and ensuring
all pairs were represented (i.e. adding the Lucas sequence, then starting at other previously-unseen pairs), that I
started started doing it for other bases: hexadecimal, octal, 7, 6, 5… And when I got home that day I wrote this
little test app to explore larger bases. Base 11 was really hard to find unseen starting pairs manually.

There is no purpose to this. It's just fun with numbers.

"""
import collections
import collections.abc
import itertools
import math
import sys
from typing import Iterable, Dict, List, Sequence, Tuple

import colorama


class Alphabet:
    """ A visual representation of a modulo fibonacci base. """
    ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyz'

    def __init__(self, base: int):
        colorama.init()
        self.length = math.ceil(math.log(base, len(self.ALPHABET)))
        symbols = sub_alphabet = self.ALPHABET[:math.ceil(base ** (1 / self.length))]
        # increment the length of each symbol until we reach the target length
        for _ in range(1, self.length):
            symbols = [ii + i for ii in symbols for i in sub_alphabet]
        self.symbols: Sequence[str] = symbols[:base]

    def dump(self, runs: Iterable[List[int]]) -> None:
        """ Prints a list of runs. Each run is assumed to represent a cycle. """
        for run in runs:
            output = [colorama.Style.BRIGHT, colorama.Fore.MAGENTA, self.symbols[run.pop()]]
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
    """ A square bitmap represeting pairs. """
    def __init__(self, side: int):
        self.side = abs(side)
        self.map = bytearray(math.ceil(side * side / 8))

    def __call__(self, n1: int, n2: int) -> bool:
        """ Visits a point, returns whether that was the first visit. """
        pos = n1 * self.side + n2
        byte_pos = pos // 8
        bit = 1 << (pos % 8)
        try:
            return bool(self.map[byte_pos] & bit)
        finally:
            self.map[byte_pos] |= bit

    def iterate_free_pairs(self) -> Iterable[Tuple[int, int]]:
        """ Yield unvisited points. """
        # index iteration to make sure iterator won't invalidate
        for byte_pos in range(len(self.map)):
            byte = self.map[byte_pos]
            for bit_pos, bit in enumerate((1, 2, 4, 8, 16, 32, 64, 128)):
                if byte & bit == 0:
                    pos = byte_pos * 8 + bit_pos
                    n1 = pos // self.side
                    if n1 >= self.side:
                        return  # Oops, we're past the end
                    n2 = pos % self.side
                    yield n1, n2
                    byte = self.map[byte_pos]  # reload byte


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
