
Modulo Fibonacci
================

Usage: ``python3 modfibo.py [BASE]``

Example: ``python3 modfibo.py 16``

[The Fibonacci sequence](https://oeis.org/A000045) is
1 1 2 3 5 8 13 21 34 55
and so on.

It's not hard to conclude that the sequence's least significant digit starts repeating after a while, but I was doing
it on paper, and it was taking way too long. For some strange reason I had so much fun doing it manually, and ensuring
all pairs were represented (i.e. adding the Lucas sequence, then starting at other previously-unseen pairs), that I
started started doing it for other bases: hexadecimal, octal, 7, 6, 5… And when I got home that day I wrote this
little test app to explore larger bases. Base 11 was really hard to find unseen starting pairs manually.

There is no purpose to this. It's just fun with numbers.
