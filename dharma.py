#import sys
import pygame
from screen import Screen


S = Screen()


def Autorun():
    S.HOME()
    # display the Swan logo
    dimx = 400
    dimy = 400
    xoff = (S.CRT_W - dimx) / 2
    yoff = 24
    swan = pygame.image.load("img/SwanLogo.png").convert_alpha()
    swan = pygame.transform.scale(swan, (dimx, dimy))
    # simulate slow loading
    speed = 2
    for i in range(0, int(dimy/speed) + 1):
        S.BLIT(swan, (xoff, yoff))
        S.HOME((xoff, yoff + speed*i, dimx, dimy))
        S._process_events()
        S.UPDATE()
    # loading prompts
    S.GOTOXY(11, 19)
    S.PRINT("STATION 3: THE SWAN")
    S.UPDATE()
    S.PAUSE(210)
    while True:
        S.GOTOXY(0, 21)
        S.PRINT("LOAD RADZINSKI.001 (Y/N)?   ")
        char = S.GETC()
        if char == 'Y':
            return True
        if char == 'N':
            return False


def StationInfo():
    S.HOME()
    # display the Swan logo
    dimx = 480
    dimy = 360
    xoff = 4
    yoff = 0
    swan = pygame.image.load("img/SwanLayout.png").convert_alpha()
    swan = pygame.transform.scale(swan, (dimx, dimy))
    # simulate slow loading
    speed = 8
    for i in range(0, int(dimy/speed) + 1):
        S.BLIT(swan, (xoff, yoff))
        S.HOME((xoff, yoff + speed*i, dimx, dimy))
        S._process_events()
        S.UPDATE()
    # map legend
    # key
    S.GOTOXY(5.2, 2)
    S.PUTC("B")
    S.GOTOXY(10, 1.5)
    S.PUTC("S")
    S.GOTOXY(16.7, 5.1)
    S.PUTC("D")
    S.GOTOXY(5.1, 5.1)
    S.PUTC("R")
    S.GOTOXY(10, 5)
    S.PUTC("H")
    S.GOTOXY(6, 7.6)
    S.PUTC("A")
    S.GOTOXY(12, 9.5)
    S.PUTC("C")
    S.GOTOXY(1, 9.6)
    S.PUTC("E")
    S.GOTOXY(19.5, 12)
    S.PUTC("E")
    S.GOTOXY(11.15, 13.4)
    S.PUTC("#")
    # key description
    S.GOTOXY(24, 0)
    S.PRINT("\ue142 bedroom area")
    S.GOTOXY(24, 1)
    S.PRINT("\ue153 storage pantry")
    S.GOTOXY(24, 2)
    S.PRINT("\ue144 computer dome")
    S.GOTOXY(24, 3)
    S.PRINT("\ue152 restroom")
    S.GOTOXY(24, 4)
    S.PRINT("\ue148 habitat/dining")
    S.GOTOXY(24, 5)
    S.PRINT("\ue141 armory")
    S.GOTOXY(24, 6)
    S.PRINT("\ue143 entry corridor")
    S.GOTOXY(24, 7)
    S.PRINT("\ue145 exit/escape")
    S.GOTOXY(24, 8)
    S.PRINT("\ue123 e.m. anomaly")
    # show basic information
    S.GOTOXY(1, 16)
    S.PRINT("The Dharma Initiative was established")
    S.GOTOXY(1, 17)
    S.PRINT("in the year of 1970.")
    S.GOTOXY(1, 19)
    S.PRINT("The Swan station's task is observation")
    S.GOTOXY(1, 20)
    S.PRINT("of electromagnetic anomalies.")
    S.GOTOXY(1, 22)
    S.PRINT("More information is provided in the")
    S.GOTOXY(1, 23)
    S.PRINT("station's orientation film.")
    S.UPDATE()
    # exit prompt
    while True:
        S.GOTOXY(25, 11)
        S.PRINT("\u2554" + "\u2550"*12 + "\u2557")
        S.GOTOXY(25, 12)
        S.PRINT("\u2551EXIT (Y/N)? \u2551")
        S.GOTOXY(25, 13)
        S.PRINT("\u255a" + "\u2550"*12 + "\u255d")
        S.GOTOXY(37, 12)
        char = S.GETC()
        if char == 'Y':
            break


def RadzinskiLoading():
    S.HOME()
    S.PRINT("LOADING")
    S.UPDATE()
    for i in range(0, 600):
        if i % 10 == 0:
            S.PUTC('.')
        S._process_events()
        S.UPDATE()
    S.HOME()
    S.UPDATE()
    for i in range(0, 60):
        S._process_events()
        S.UPDATE()


def JacobsList():
    S.HOME()
    S.GOTOXY(2, 2)
    S.PRINT(' 4 – Locke')
    S.GOTOXY(2, 4)
    S.PRINT(' 8 – Reyes')
    S.GOTOXY(2, 6)
    S.PRINT('15 – Ford')
    S.GOTOXY(2, 8)
    S.PRINT('16 – Jarrah')
    S.GOTOXY(2, 10)
    S.PRINT('23 – Shephard')
    S.GOTOXY(2, 12)
    S.PRINT('42 – Kwon')
    S.GOTOXY(2, 20)
    S.PRINT('PRESS ANY KEY TO CONTINUE...')
    while True:
        char = S.GETC()
        break


def SystemFailure():
    S.GOTOXY(0, 1)
    while True:
        S.PRINT("SYSTEM FAILURE ")
        S.PAUSE(4)
        S.UPDATE()


def TimerReset():
    S.BEEP()
    S.SOUND("timerr", 1)


def ButtonLoop():
    commands = {
        "4 8 15 16 23 42": TimerReset,
        "INFO": StationInfo,
        "JACOB": JacobsList
    }
    while True:
        S.HOME()
        S.PRINT(">:")
        string = S.INPUT().strip()
        if string not in commands:
            break
        commands[string]()
    SystemFailure()


if __name__ == '__main__':
    if Autorun():
        RadzinskiLoading()
        ButtonLoop()
