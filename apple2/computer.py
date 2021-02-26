"""
Simulates the Apple III computer
"""

import sys
import pygame
import os
from math import pi, sin
from pygame.locals import *


__all__ = ['Computer']


class Computer:

    # width and height of the Apple III monitor background image
    MON_IMG_W = 1400
    MON_IMG_H = 792
    # widgh and height of the CRT viewframe
    CRT_W = 840
    CRT_H = 576
    # offset of the CRT viewframe
    CRT_X = 137
    CRT_Y = 105
    # actual Apple III monitor horiz and vert. resolution
    XRES = 280
    YRES = 192
    # CRT parameters
    DECAY = 254
    REFRESH = 60


    def __init__(self):

        # initialize pygame app
        pygame.init()
        pygame.key.set_repeat(500, 60)
        pygame.display.set_caption("Scanlines")
        self.screen = pygame.display.set_mode((self.MON_IMG_W, self.MON_IMG_H))
        pygame.display.set_caption("DHARMA Swan Computer")

        # load background image
        self.background = pygame.image.load("IMG/APPLEIII.PNG").convert_alpha()

        # load Apple II fonts
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.font = pygame.font.Font(os.path.join(dir_path, "font", "PrintChar21.ttf"), 24)
        self.font2 = pygame.font.SysFont("Arial", 18)

        # set default color: https://en.wikipedia.org/wiki/Phosphor#Standard_phosphor_types
        self.color = pygame.Color("#33ff33ff")

        # set initial cursor location
        self.cursorx = 0
        self.cursory = 0
        self.blockcursor = 0

        # use internal clock for controling refresh rate
        self.clock = pygame.time.Clock()

        # initialize the CRT buffers (two for blending effect)
        self.crt0 = pygame.Surface([self.CRT_W, self.CRT_H], pygame.SRCALPHA, 32).convert_alpha()
        self.crt1 = pygame.Surface([self.CRT_W, self.CRT_H], pygame.SRCALPHA, 32).convert_alpha()

        # create the horizontal scanline mask
        self.scanlines = pygame.Surface([self.CRT_W, self.CRT_H], pygame.SRCALPHA, 32).convert_alpha()
        for i in range(0, self.CRT_H):
            f = (i % 3) / 3
            col = 255*(1 - abs(sin(pi*f))**2.5)
            pygame.draw.line(self.scanlines, (0, 0, 0, col), (0, i), (self.CRT_W, i))

        # load sound effects
        self.sounds = { "click":  pygame.mixer.Sound("SND/CLICK.MP3"),
                        "beep":   pygame.mixer.Sound("SND/BEEP.MP3"),
                        "dharma": pygame.mixer.Sound("SND/DHARMA.MP3"),
                        "timerr": pygame.mixer.Sound("SND/TIMERRESET.MP3") }


    def __process_events(self):
        for event in pygame.event.get():
            # quit request
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # key pressed
            if event.type == KEYDOWN:
                self.__play("click", 0.5)
                return event
        return None


    def __play(self, snd, volume):
        snd = self.sounds[snd]
        if snd is not None:
            snd.set_volume(volume)
            snd.play()


    def __beep(self):
        self.__play("beep", 0.5)


    def __fps(self):
	    fps = str(int(self.clock.get_fps()))
	    fps_text = self.font2.render(fps, 1, pygame.Color("coral"))
	    return fps_text


    def __scroll(self):
        self.crt1.scroll(0, -24)
        pygame.draw.rect(self.crt1, (0, 0, 0, 0), (0, 23*24, self.CRT_W, 24))


    def __putc(self, char, fwd=True):
        if char == chr(7):
            self.__beep()
            return None
        x0 = self.cursorx*21
        y0 = self.cursory*24
        pygame.draw.rect(self.crt1, (0, 0, 0), (x0, y0, 21, 24))
        if char is not None:
            if self.font.size(char)[0] > 0:
                text = self.font.render(char, 1, self.color)
                self.crt1.blit(text, (x0, y0))
        if fwd:
            self.cursorx += 1
            if self.cursorx >= 40:
                self.cursorx = 0
                self.cursory += 1
            if self.cursory >= 24:
                self.__scroll()
                self.cursory = 23


    def __idle(self):
        self.__process_events()
        self.__update()


    def __update(self):
        self.screen.blit(self.background, (0, 0))
        self.crt0.fill((0, 32, 0))
        self.crt0.blit(self.crt1, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        self.crt0.blit(self.scanlines, (0, 0))
        self.screen.blit(self.crt0, (self.CRT_X, self.CRT_Y))
        self.screen.blit(self.__fps(), (10, 0))
        pygame.event.pump()
        pygame.display.flip()
        self.clock.tick(self.REFRESH)


    def htab(self, x):
        x -= 1
        if x < 0:
            self.cursorx = 0
        elif x >= 40:
            self.cursorx = 39
        else:
            self.cursorx = x


    def vtab(self, y):
        y -= 1
        if y < 0:
            self.cursory = 0
        elif y >= 24:
            self.cursory = 23
        else:
            self.cursory = y


    def clrscr(self, rect=None):
        if rect is None:
            self.crt1.fill((0, 0, 0, 0))
            self.cursorx = 0
            self.cursory = 0
        else:
            pygame.draw.rect(self.crt1, (0, 0, 0, 0), rect)


    def getc(self, echo=False):
        time = pygame.time.get_ticks()
        i = 0
        while True:
            event = self.__process_events()
            if event is not None:
                char = pygame.key.name(event.key).upper()
                if char == "SPACE":
                    char =  ' '
                if char == "RETURN":
                    if echo:
                        self.__putc(None, fwd=False)
                    return ''
                elif char == "BACKSPACE" and echo:
                    if self.cursory > self.blockcursor[1] or self.cursorx > self.blockcursor[0]:
                        self.__putc(None, fwd=False)
                        if self.cursorx > 0:
                            self.cursorx -= 1
                        else:
                            self.cursorx = 39
                            self.cursory -= 1
                    return -1
                elif len(char) == 1:
                    # handle shift key modifier
                    if event.mod & pygame.KMOD_LSHIFT or event.mod & pygame.KMOD_RSHIFT:
                        if char == '2':
                            char = '"'
                        elif char == '3':
                            char = '#'
                        elif char == '4':
                            char = '$'
                        elif char == '5':
                            char = '%'
                        elif char == '6':
                            char = '&'
                        elif char == '7':
                            char = '/'
                        elif char == '8':
                            char = '('
                        elif char == '9':
                            char = ')'
                        elif char == '0':
                            char = '='
                        elif char == '\'':
                            char = '?'
                        elif char == '+':
                            char = '*'
                        elif char == '<':
                            char = '>'
                        elif char == ',':
                            char = ';'
                        elif char == '.':
                            char = ':'
                        elif char == '-':
                            char = '_'
                    elif event.mod & K_LALT or event.mod & K_RALT:
                        if char == '3':
                            char = '^'
                    if echo:
                        self.__putc(char)
                        self.__update()
                    return char
            if echo:
                newtime = pygame.time.get_ticks()
                if newtime - time >= 200:
                    i += 1
                    time = newtime
                self.__putc(['\u2588', None][i % 2], fwd=False)
                self.__update()


    def input(self, end=True):
        self.blockcursor = (self.cursorx, self.cursory)
        string = ""
        while True:
            char = self.getc(echo=True)
            if char == '':
                break
            elif char == -1:
                string = string[0:(len(string) - 1)]
            else:
                string += char
        self.blockcursor = (0, 0)
        if end:
            self.print(end=True, flush=True)
        return string


    def print(self, string='', end=True, flush=True):
        for char in string:
            self.__putc(char)
        if end:
            self.cursorx = 0
            self.cursory += 1
            if self.cursory >= 24:
                self.__scroll()
                self.cursory = 23
        if flush:
            self.__update()


    def img(self, imgfilename, xpos, ypos, scale, speed):
        if scale == None:
            scale = 3

        imgfile = pygame.image.load(imgfilename).convert_alpha()
        dimx, dimy = tuple(map((scale).__mul__, imgfile.get_size()))
        imgfile = pygame.transform.scale(imgfile, (int(dimx), int(dimy)))

        # Immediate blit
        if speed == None:
            self.crt1.blit(imgfile, (xpos, ypos))

        # Simulate slow loading
        else:
            for i in range(0, int(dimy/speed) + 1):
                self.crt1.blit(imgfile, (xpos, ypos))
                self.clrscr((xpos, ypos + speed*i, dimx, dimy))
                self.__idle()


    def snd(self, sndfilename, vol):
        if vol == None:
            vol = 1

        sndfile = pygame.mixer.Sound(sndfilename)
        sndfile.set_volume(vol)
        sndfile.play()


    def pause(self, delay):
        if delay < 0:
            rep = sys.maxsize
        else:
            rep = int(delay * self.REFRESH)
        for i in range(0, rep):
            self.__idle()
