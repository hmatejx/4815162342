"""
Emulates the Apple III monitor
"""

import sys
from math import pi, cos, sin
import pygame
from pygame.locals import *


__all__ = ['Screen']


class Screen:

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
        self.background = pygame.image.load("img/Apple]I[.png").convert_alpha()

        # load Apple II fonts
        self.font = pygame.font.Font("font/PrintChar21.ttf", 24)
        self.font2 = pygame.font.SysFont("Arial", 18)

        # set default color: https://en.wikipedia.org/wiki/Phosphor#Standard_phosphor_types
        self.color = pygame.Color("#33ff33ff")

        # set initial cursor location
        self.cursorx = 0
        self.cursory = 0
        self.blockcursor = 0

        # initialize the CRT buffers (two for blending effect)
        self.crt0 = pygame.Surface([self.CRT_W, self.CRT_H], pygame.SRCALPHA, 32).convert_alpha()
        self.crt1 = pygame.Surface([self.CRT_W, self.CRT_H], pygame.SRCALPHA, 32).convert_alpha()

        # create the horizontal scanline mask
        self.scanlines = pygame.Surface([self.CRT_W, self.CRT_H], pygame.SRCALPHA, 32).convert_alpha()
        for i in range(0, self.CRT_H):
            f = (i % 3) / 3
            col = 255*(1 - abs(sin(pi*f))**2.5)
            pygame.draw.line(self.scanlines, (0, 0, 0, col), (0, i), (self.CRT_W, i))

        # use internal clock for refresh
        self.Clock = pygame.time.Clock()

        # load sound effects
        self.sounds = { "click":  pygame.mixer.Sound("snd/click.mp3"),
                        "beep":   pygame.mixer.Sound("snd/beep.mp3"),
                        "dharma": pygame.mixer.Sound("snd/dharma.mp3"),
                        "timerr": pygame.mixer.Sound("snd/timer_reset.mp3") }
        self.SOUND("beep", 0.5)
        self.SOUND("dharma", 0.5)


    def PUTC(self, char):
        x0 = self.cursorx*21
        y0 = self.cursory*24
        pygame.draw.rect(self.crt1, (0, 0, 0), (x0, y0, 21, 24))
        if char is not None:
            if self.font.size(char)[0] > 0:
                text = self.font.render(char, 1, self.color)
                self.crt1.blit(text, (x0, y0))
        self.cursorx += 1
        if self.cursorx >= 40:
            self.cursorx = 0
            self.cursory += 1
        if self.cursory >= 24:
            self.crt1.blit(self.crt1, (0, -24))
            self.cursory = 23


    def _process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                self.SOUND("click", 0.5)
                return event
        return None


    def _wait_for_keypress(self):
        while True:
            if self._process_events() is not None:
                break


    def GETC(self):
        time = pygame.time.get_ticks()
        i = 0
        while True:
            event = self._process_events()
            if event is not None:
                char = pygame.key.name(event.key).upper()
                if char == "SPACE":
                    char =  ' '
                if char == "RETURN":
                    return ''
                elif char == "BACKSPACE":
                    if self.cursory > self.blockcursor[1]:
                        if self.cursorx > 0:
                            self.PUTC(None)
                            self.cursorx -= 2
                        else:
                            self.PUTC(None)
                            self.cursorx = 39
                            self.cursory -= 1                            
                    else:
                        if self.cursorx > self.blockcursor[0]:
                            self.PUTC(None)
                            if self.cursorx == 0:
                                self.cursorx = 38
                                self.cursory -= 1
                            else:
                                self.cursorx -= 2
                    return -1
                elif len(char) == 1:
                    self.PUTC(char)
                    self.UPDATE()
                    return char
            newtime = pygame.time.get_ticks()
            if newtime - time >= 200:
                i += 1
                time = newtime
            self.PUTC(['\u2588', None][i % 2])
            self.UPDATE()
            if self.cursorx > 0:
                self.cursorx -= 1
            else:
                self.cursorx = 39
                self.cursory -= 1


    def INPUT(self):
        self.blockcursor = (self.cursorx, self.cursory)
        string = ""
        while True:
            char = self.GETC()
            if char == '':
                break
            elif char == -1:
                string = string[0:(len(string) - 1)]
            else:
                string += char
        self.blockcursor = (0, 0)
        print(string)
        return string


    def PRINT(self, string):
        for char in string:
            self.PUTC(char)


    def GOTOXY(self, x, y):
        if x < 0:
            x = 0
        if x > 39:
            x = 39
        if y < 0:
            y = 0
        if y > 23:
            y = 23
        self.cursorx = x
        self.cursory = y


    def BLIT(self, img, pos):
        self.crt1.blit(img, pos)


    def HOME(self, rect = None):
        if rect is None:
            self.crt1.fill((0, 0, 0, 0))
            self.GOTOXY(0, 0)
        else:
            pygame.draw.rect(self.crt1, (0, 0, 0, 0), rect)


    def UPDATE(self):
        self.screen.blit(self.background, (0, 0))
        self.crt0.fill((0, 12, 0), special_flags=pygame.BLEND_RGB_ADD)
        self.crt0.blit(self.crt1, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)
        self.crt0.blit(self.scanlines, (0, 0))
        self.screen.blit(self.crt0, (self.CRT_X, self.CRT_Y))
        self.screen.blit(self._fps(), (10, 0))
        pygame.display.flip()
        self.Clock.tick(self.REFRESH)


    def PAUSE(self, rep):
        for i in range(0, rep):
            self._process_events()
            self.UPDATE()


    def BEEP(self):
        self.SOUND("beep", 0.5)


    def SOUND(self, snd, volume):
        snd = self.sounds[snd]
        if snd is not None:
            snd.set_volume(volume)
            snd.play()


    def _fps(self):
	    fps = str(int(self.Clock.get_fps()))
	    fps_text = self.font2.render(fps, 1, pygame.Color("coral"))
	    return fps_text
