"""
Computer simulator "interface" class. It
implements the default computer (terminal) so
that the interpreter can be used directly.

If you want to implement your own computer simulator,
implement the following functions in your simulator.

For the exact interface definition, look at the
implementation in apple2/computer.py

"""

import readchar
import time


class TerminalComputer:
    def __init__(self):
        self.print = print
        self.input = input
        self.getc = readchar.readchar  # msvcrt.getch
        self.clrscr = lambda *args, **kwargs: None
        self.htab = lambda *args, **kwargs: None
        self.vtab = lambda *args, **kwargs: None
        self.img = lambda *args, **kwargs: None
        self.snd = lambda *args, **kwargs: None
        self.pause = time.sleep
