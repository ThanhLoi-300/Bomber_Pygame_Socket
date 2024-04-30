import pygame

from src.model.Actor import Actor


class Box:
    ALLROW_BANG = 0
    DISALLROW_BANG = 1

    def __init__(self, x, y, box_type, image_path):
        self.x = x + 4
        self.y = y
        self.box_type = box_type
        self.img = image_path
        self.width = pygame.image.load("../" + str(self.img)).convert_alpha().get_width()
        self.height = pygame.image.load("../" + str(self.img)).convert_alpha().get_height()

    def drawBox(self, screen):
        img = pygame.image.load("../" + str(self.img)).convert_alpha()
        img = pygame.transform.scale(img, (
            self.width, self.height))
        screen.blit(img, (self.x, self.y))

    # Kiểm tra va chạm giữa actor vs các box
    def isImpactBoxvsActor(self, actor):
        rect1 = pygame.Rect(self.x + 4, self.y, self.width - 8, self.height - 4)
        rect2 = pygame.Rect(actor.x, actor.y, actor.width, actor.height)
        rect3 = rect1.clip(rect2)

        if rect1.colliderect(rect2):
            print("true")
            if rect3.height == 1 and (actor.orient == Actor.UP or actor.orient == Actor.DOWN):
                if actor.x == rect3.x:
                    return rect3.width
                else:
                    return -rect3.width
            else:
                if actor.y == rect3.y:
                    return rect3.height
                else:
                    return -rect3.height

        return 0

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height
