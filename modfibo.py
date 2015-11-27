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
from collections import defaultdict
from sys import argv, stdout

ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_/+=!?@#$%^&*;,.:"\'\\`~(){}<>|'


class VisitedMap:
    def __init__(self, side):
        self.side = abs(int(side))
        self.map = 0

    def __call__(self, n1, n2):
        pos = n1 * self.side + n2
        mask = 1 << pos
        try:
            return bool(self.map & mask)
        finally:
            self.map |= mask

    def inform(self, that):
        that.map |= self.map

    def find_pair(self):
        length = self.side * self.side
        mask = (1 << length) - 1
        search = mask ^ self.map
        if search == 0:
            return None
        pos = 0
        while not search & 1:
            search >>= 1
            pos += 1
        return pos // self.side, pos % self.side


class ModuloFibonacci:
    def __init__(self, mod):
        self.mod = int(mod)
        if mod <= 0:
            raise ValueError('Mod must be positive.')
        self.visited = VisitedMap(self.mod)

    def run(self, n1, n2):
        visited = VisitedMap(self.mod)
        while not visited(n1, n2):
            n1, n2 = n2, (n1 + n2) % self.mod
            yield n1
        visited.inform(self.visited)

    def run_through(self):
        pair = self.visited.find_pair()
        while pair:
            assert isinstance(pair, tuple)
            run = tuple(self.run(*pair))
            yield pair, run
            pair = self.visited.find_pair()


def main(mf):
    histogram = defaultdict(int)
    for initial, sequence in mf.run_through():
        colors(1, 35)
        numbers(initial[0])
        colors(36)
        numbers(*sequence)
        colors(0)
        print('')
        histogram[len(sequence)] += 1
    print('%d sequences.' % sum(histogram.values()))
    print('; '.join(('%d of %d' % (amount, length) for (length, amount) in sorted(histogram.items()))))


def colors(*codes):
    stdout.write('\033[%sm' % ';'.join(map(str, codes)))


def numbers(*values):
    chars = map(lambda x: ALPHABET[x], values)
    stdout.write(''.join(chars))


if __name__ == '__main__':
    try:
        base = int(argv[-1])
    except ValueError:
        base = 10
    if base <= 0:
        print("Base must be positive.")
    elif base > len(ALPHABET):
        print("Settle down! I can't represent more than %d digits." % len(ALPHABET))
    else:
        main(ModuloFibonacci(base))
