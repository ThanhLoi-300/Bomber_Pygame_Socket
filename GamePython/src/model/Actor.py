import pygame


class Actor:
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    ALIVE = 1
    DEAD = 0
    BOMBER = 1
    BOMB = 4
    x, y, type, orient, speed, width, height, run_bomb = 0, 0, 0, 0, 0, 0, 0, 0
    image = ""
    ALLOW_RUN = 0
    DISALLOW_RUN = 1

    def __init__(self, x, y, actor_type, orient, speed, sizebomb, quantityBomb, imgName, name, heart):
        self.sizeBomb = sizebomb
        self.quantity_bomb = quantityBomb
        self.x = x
        self.y = y
        self.type = actor_type
        self.orient = orient
        self.speed = speed
        self.run_bomb = self.DISALLOW_RUN
        self.img = imgName
        self.width = pygame.image.load("../Images/" + self.img + ".png").get_width()
        self.height = pygame.image.load("../Images/" + self.img + ".png").get_height() - 11
        self.status = self.ALIVE
        self.name = name
        self.heart = heart

        # Tạo font cho tên
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)  # Thay đổi None và 24 để tùy chỉnh font và kích thước

    def draw_actor(self, screen):
        img = pygame.image.load("../Images/" + self.img + ".png")
        screen.blit(img, (self.x, self.y - 11))

        # Vẽ tên
        text_surface = self.font.render(self.name, True,
                                        (255, 255, 255))  # Thay đổi (255, 255, 255) để tùy chỉnh màu sắc
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.x + self.width // 2, self.y - 30)
        screen.blit(text_surface, text_rect)

        # Vẽ heart
        if self.heart > 0:
            heart = pygame.image.load("../Images/heart_1.png")
            for i in range(self.heart):
                space = i * heart.get_width() - 20
                heart_react = heart.get_rect()
                heart_react.midtop = (self.x + self.width // 2 + space, self.y - 50)
                screen.blit(heart, heart_react)

    def is_impact_bomber_vs_actor(self, actor):
        if self.status == self.DEAD:
            return False
        rec1 = pygame.Rect(self.x, self.y, self.width, self.height)
        rec2 = pygame.Rect(actor.get_x(), actor.get_y(), actor.get_width(), actor.get_height())
        return rec1.colliderect(rec2)

    def move(self, arr_bomb, arr_box):
        if self.status == self.DEAD:
            return False

        if self.orient == self.LEFT:
            if self.x < 45:
                return False
            self.x -= self.speed
            for bomb in arr_bomb:
                if bomb.isImpactBombvsActor(self) == 1:
                    self.x += self.speed
                    return False
            for box in arr_box:
                kq = box.isImpactBoxvsActor(self)
                if kq != 0:
                    self.x += self.speed
                    return False

        elif self.orient == self.RIGHT:
            if self.x > (720 - self.width):
                return False
            self.x += self.speed
            for bomb in arr_bomb:
                if bomb.isImpactBombvsActor(self) == 1:
                    self.x -= self.speed
                    return False
            for box in arr_box:
                kq = box.isImpactBoxvsActor(self)
                if kq != 0:
                    self.x -= self.speed
                    return False

        elif self.orient == self.UP:
            if self.y < 45:
                return False
            self.y -= self.speed
            for bomb in arr_bomb:
                if bomb.isImpactBombvsActor(self) == 1:
                    self.y += self.speed
                    return False
            for box in arr_box:
                kq = box.isImpactBoxvsActor(self)
                if kq != 0:
                    self.y += self.speed
                    return False

        elif self.orient == self.DOWN:
            if self.y > 630 - self.height:
                return False
            self.y += self.speed
            for bomb in arr_bomb:
                if bomb.isImpactBombvsActor(self) == 1:
                    self.y -= self.speed
                    return False
            for box in arr_box:
                kq = box.isImpactBoxvsActor(self)
                if kq != 0:
                    self.y -= self.speed
                    return False

        return True

    def changeOrient(self, orient, imgName, screen):
        if self.status == self.DEAD:
            return

        self.orient = orient
        self.img = imgName

        self.draw_actor(screen)

    def setQuantityBomb(self, quantity_bomb):
        if quantity_bomb > 10:
            return
        self.quantity_bomb = quantity_bomb

    def setSizeBomb(self, sizeBomb):
        if sizeBomb > 10:
            return
        self.sizeBomb = sizeBomb

    def setSpeed(self, speed):
        if speed < 1:
            return
        self.speed = speed

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_orient(self):
        return self.orient

    def set_run_bomb(self, run_bomb):
        self.run_bomb = run_bomb

    def get_run_bomb(self):
        return self.run_bomb

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        if speed < 1:
            return
        self.speed = speed

    def get_type(self):
        return self.type
