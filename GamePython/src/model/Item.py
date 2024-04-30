import pygame

from src.model.Actor import Actor


class Item:
    Item_Bomb = 1
    Item_BombSize = 2
    Item_Shoe = 3

    def __init__(self, x, y, type, image):
        self.x = x + 4
        self.y = y
        self.type = type
        self.img = pygame.image.load("../" + image).convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.timeLine = 250

    def drawItem(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getTimeLine(self):
        return self.timeLine

    def setTimeLine(self, timeLine):
        self.timeLine = timeLine

    def isImpactItemVsBomber(self, actor):
        rect1 = pygame.Rect(self.x, self.y, self.width, self.height)
        rect2 = pygame.Rect(actor.x, actor.y, actor.width, actor.height)
        return rect1.colliderect(rect2)
