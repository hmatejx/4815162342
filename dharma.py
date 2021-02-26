#! /usr/bin/python

from pybasic.basicparser import BASICParser
from pybasic.lexer import Lexer
from pybasic.program import Program
from apple2.computer import Computer
import pygame
import sys


#lexer = Lexer()
computer = Computer()
parser = BASICParser(computer)
program = Program(parser)


def quit():
    pygame.quit()
    sys.exit()


def ButtonLoop():
    commands = {
        "4 8 15 16 23 42": "BAS/TIMERRESET.BAS",
        "INFO": "BAS/STATIONINFO.BAS",
        "JACOB": "BAS/JACOB.BAS"
    }
    while True:
        computer.clrscr()
        computer.print(">:", end=False)
        string = computer.input().strip()
        if string in commands:
            program.load(commands[string])
            program.execute()


if __name__ == "__main__":
    program.load("BAS/AUTORUN.BAS")
    if program.execute() == 1:
        ButtonLoop()
