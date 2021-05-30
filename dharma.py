#! /usr/bin/python

from pybasic.interpreter import Interpreter
from apple2.computer import Computer as AppleII
import pygame
import sys


# Link the Apple II simulator with the pybasic interpreter
computer = AppleII()
interpreter = Interpreter(computer)


def ButtonLoop():
    # Dictionary of implemented commands
    commands = {
        "4 8 15 16 23 42": "DHARMA/TIMERRESET.BAS",
        "INFO": "DHARMA/STATIONINFO.BAS",
        "JACOB": "DHARMA/JACOB.BAS",
        "BASIC": interpreter.interactive
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
            # load and execute a BASIC program
            elif isinstance(target, str) and target.find(".BAS"):
                interpreter.load(target)
                interpreter.execute()


if __name__ == "__main__":
    interpreter.load("DHARMA/AUTORUN.BAS")
    if interpreter.execute() == 1:
        ButtonLoop()
