import pygame

from src.model.Actor import Actor
import time


class Bomb:
    def __init__(self, x, y, size, timeline):
        self.x = (x // 45) * 45
        self.y = (y // 45) * 45
        self.size = size
        self.orient = 0
        self.timeline = time.time() + timeline
        self.type = Actor.BOMB
        self.img = pygame.image.load("../Images/bomb.gif").convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def drawActor(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def deadlineBomb(self):
        if time.time() >= self.timeline:
            self.timeline = 0

    def getTimeline(self):
        return self.timeline

    def getSize(self):
        return self.size

    def setRun(self, actor):
        rect2 = pygame.Rect(self.x, self.y, 45, 45)
        rect3 = pygame.Rect(actor.x, actor.y, actor.width, actor.height)
        return rect2.colliderect(rect3)

    def setTimeline(self, timeline):
        self.timeline = timeline

    def isImpact(self, xNewBomb, yNewBomb):
        rect1 = pygame.Rect(self.x, self.y, 45, 45)
        rect2 = pygame.Rect(xNewBomb, yNewBomb, 45, 45)
        return rect1.colliderect(rect2)

    def isImpactBombvsActor(self, actor):
        if actor.run_bomb == Actor.ALLOW_RUN:
            return 0
        rect2 = pygame.Rect(self.x, self.y, 45, 45)
        rect3 = pygame.Rect(actor.x, actor.y, actor.width, actor.height)
        if rect2.colliderect(rect3):
            return 1
        return 0
