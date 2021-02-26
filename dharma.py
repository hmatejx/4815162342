#! /usr/bin/python

from pybasic.basicparser import BASICParser
from pybasic.lexer import Lexer
from pybasic.program import Program
from apple2.computer import Computer
from interpreter import Interpreter
import pygame
import sys


computer = Computer()
parser = BASICParser(computer)
program = Program(parser)


def quit():
    pygame.quit()
    sys.exit()


def ButtonLoop():
    # Dictionary of implemented commands
    commands = {
        "4 8 15 16 23 42": "BAS/TIMERRESET.BAS",
        "INFO": "BAS/STATIONINFO.BAS",
        "JACOB": "BAS/JACOB.BAS",
        "BASIC": Interpreter
    }
    while True:
        # Get user input
        computer.clrscr()
        computer.print(">:", end=False)
        string = computer.input().strip()
        # Find the input in the dictionary
        if string in commands:
            target = commands[string]
            # call a Python function
            if callable(target):
                computer.pause(1)
                target()
                computer.pause(1)
            # run a BASIC program
            elif isinstance(target, str) and target.find(".BAS"):
                program.load(target)
                program.execute()


if __name__ == "__main__":
    program.load("BAS/AUTORUN.BAS")
    if program.execute() == 1:
        ButtonLoop()
