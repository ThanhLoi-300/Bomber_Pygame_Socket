import time

import pygame
from pygame.locals import *
from src.model import Bomb, Item
from src.model.Actor import Actor
from src.model.Box import Box


class BombBang:
    def __init__(self, x, y, size, arrBox):
        self.x = x
        self.y = y
        self.size = size
        self.timeLine = time.time() + 0.25
        self.img_left = pygame.image.load("../Images/bombbang_left1.png")
        self.img_right = pygame.image.load("../Images/bombbang_right1.png")
        self.img_up = pygame.image.load("../Images/bombbang_up1.png")
        self.img_down = pygame.image.load("../Images/bombbang_down1.png")
        for i in range(1, size):
            tmp_left = 0
            tmp_right = 0
            tmp_up = 0
            tmp_dow = 0
            for j in range(len(arrBox)):
                if self.isImpactBox(x - i * 45, y, (i + 1) * 45, 45, arrBox[j]):
                    tmp_left = 1
                if self.isImpactBox(x, y, (i + 1) * 45, 45, arrBox[j]):
                    tmp_right = 1
                if self.isImpactBox(x, y - (i * 45), 45, (i + 1) * 45, arrBox[j]):
                    tmp_up = 1
                if self.isImpactBox(x, y, 45, (i + 1) * 45, arrBox[j]):
                    tmp_dow = 1
            if tmp_left == 0:
                self.setImage(Actor.LEFT, i + 1)
            if tmp_right == 0:
                self.setImage(Actor.RIGHT, i + 1)
            if tmp_up == 0:
                self.setImage(Actor.UP, i + 1)
            if tmp_dow == 0:
                self.setImage(Actor.DOWN, i + 1)

    def drawBongBang(self, screen):
        screen.blit(self.img_left, (self.x + 45 - self.img_left.get_width(), self.y))
        screen.blit(self.img_right, (self.x, self.y))
        screen.blit(self.img_up, (self.x, self.y + 45 - self.img_up.get_height()))
        screen.blit(self.img_down, (self.x, self.y))

    def isImpactBox(self, x, y, width, height, box):
        rec1 = Rect(x, y, width, height)
        rec2 = Rect(box.x, box.y, box.width, box.height)
        return rec1.colliderect(rec2)

    def isImpactBombBangVsActor(self, actor):
        rec1 = Rect(self.x + 45 - self.img_left.get_width(), self.y + 5, self.img_left.get_width() - 5,
                    self.img_left.get_height() - 10)
        rec2 = Rect(self.x, self.y + 5, self.img_right.get_width() - 5, self.img_right.get_height() - 10)
        rec3 = Rect(self.x + 5, self.y + 45 - self.img_up.get_height() + 5, self.img_up.get_width() - 5,
                    self.img_up.get_height() - 10)
        rec4 = Rect(self.x + 5, self.y, self.img_down.get_width() - 10, self.img_down.get_height() - 5)
        rec5 = Rect(actor.x, actor.y, actor.width, actor.height)
        if rec1.colliderect(rec5) or rec2.colliderect(rec5) or rec3.colliderect(rec5) or rec4.colliderect(rec5):
            return True
        return False

    def isImpactBombBangvsBomb(self, bomb):
        rec1 = Rect(self.x + 45 - self.img_left.get_width(), self.y, self.img_left.get_width(),
                    self.img_left.get_height())
        rec2 = Rect(self.x, self.y, self.img_right.get_width(), self.img_right.get_height())
        rec3 = pygame.Rect(self.x + 9, self.y + 45 - self.img_up.get_height(), self.img_up.get_width() - 9,
                           self.img_up.get_height())
        rec4 = pygame.Rect(self.x + 9, self.y, self.img_down.get_width() - 9, self.img_down.get_height())
        rec5 = Rect(bomb.x, bomb.y, bomb.width, bomb.height)
        if rec1.colliderect(rec5) or rec2.colliderect(rec5) or rec3.colliderect(rec5) or rec4.colliderect(rec5):
            return True
        return False

    def isImpactBombBangvsBox(self, box):
        if box.box_type == Box.DISALLROW_BANG:
            return False

        rec1 = pygame.Rect(self.x + 45 - self.img_left.get_width(), self.y, self.img_left.get_width(),
                           self.img_left.get_height())
        rec2 = pygame.Rect(self.x, self.y, self.img_right.get_width(), self.img_right.get_height())
        rec3 = pygame.Rect(self.x + 9, self.y + 45 - self.img_up.get_height(), self.img_up.get_width() - 9,
                           self.img_up.get_height())
        rec4 = pygame.Rect(self.x + 9, self.y, self.img_down.get_width() - 9, self.img_down.get_height())
        rec5 = pygame.Rect(box.x, box.y, box.width, box.height)

        if rec1.colliderect(rec5) or rec2.colliderect(rec5) or rec3.colliderect(rec5) or rec4.colliderect(rec5):
            return True

        return False

    def isImpactBombBangvsItem(self, item):
        rec1 = pygame.Rect(self.x + 45 - self.img_left.get_width(), self.y, self.img_left.get_width(),
                           self.img_left.get_height())
        rec2 = pygame.Rect(self.x, self.y, self.img_right.get_width(), self.img_right.get_height())
        rec3 = pygame.Rect(self.x, self.y + 45 - self.img_up.get_height(), self.img_up.get_width(),
                           self.img_up.get_height())
        rec4 = pygame.Rect(self.x, self.y, self.img_down.get_width(), self.img_down.get_height())
        rec5 = pygame.Rect(item.x, item.y, item.width, item.height)

        if rec1.colliderect(rec5) or rec2.colliderect(rec5) or rec3.colliderect(rec5) or rec4.colliderect(rec5):
            if item.getTimeLine() > 0:
                item.setTimeLine(item.getTimeLine() - 1)
                return False
            else:
                return True

        return False

    def setImage(self, orient, size):
        if orient == Actor.LEFT:
            self.img_left = pygame.image.load("../Images/bombbang_left"+str(size)+".png").convert_alpha()
        elif orient == Actor.RIGHT:
            self.img_right = pygame.image.load("../Images/bombbang_right"+str(size)+".png").convert_alpha()
        elif orient == Actor.UP:
            self.img_up = pygame.image.load("../Images/bombbang_up"+str(size)+".png").convert_alpha()
        elif orient == Actor.DOWN:
            self.img_down = pygame.image.load("../Images/bombbang_down"+str(size)+".png").convert_alpha()

    def deadlineBomb(self):
        if time.time() >= self.timeLine:
            self.timeLine = 0
