import json
import time
import traceback

import pygame
from pygame.locals import *
import random

from src.model.Actor import Actor
from src.model.Bomb import Bomb
from src.model.BombBang import BombBang
from src.model.Box import Box
from src.model.Item import Item

import threading


class EnterGame:
    def __init__(self, screen, typeActor, name, client_socket):
        pygame.init()
        self.random = random.Random()
        self.arrBox = []
        self.arrBomb = []
        self.arrBombBang = []
        self.arrItem = []
        self.Background = ""
        self.status = 0
        self.typeActor = typeActor

        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.screen = screen
        self.imgName = ""
        self.name = name
        self.client_socket = client_socket
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        self.running = True
        self.lock = threading.Lock()

        self.main_Image = pygame.image.load("../Images/background_Play3.png")
        self.main_Image = pygame.transform.scale(self.main_Image, (
            self.WIDTH + 215, self.HEIGHT))  # Chia tỷ lệ hình ảnh để phù hợp với màn hình

        # Dialog hiển thị tên
        self.dialog_text = self.font.render("You Lose", True, (255, 0, 0))
        self.dialog_rect = pygame.Rect((self.WIDTH - 200) // 2, (self.HEIGHT - 200) // 2, 200, 200)
        self.showDialog = False

        self.mBomber = None

        if self.typeActor == 1:
            self.imgName = "bebong_down"
            self.mBomber = Actor(60, 350, Actor.BOMBER, Actor.DOWN, 5, 1, 1, self.imgName, self.name, 3)
        else:
            self.imgName = "khokho_down"
            self.mBomber = Actor(680, 350, Actor.BOMBER, Actor.DOWN, 5, 1, 1, self.imgName, self.name, 3)

        self.other = None

        self.press_a = False
        self.press_s = False
        self.press_d = False
        self.press_w = False

        self.drawMap = True
        self.is_sending_data = False

    def run(self):
        # Tạo một luồng riêng để nhận phản hồi từ máy chủ
        response_thread = threading.Thread(target=self.receive_response_from_server)
        response_thread.start()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_a:
                        # Xử lý sự kiện nhấn phím "a"
                        self.press_a = True
                    elif event.key == K_s:
                        # Xử lý sự kiện nhấn phím "s"
                        self.press_s = True
                    elif event.key == K_d:
                        # Xử lý sự kiện nhấn phím "d"
                        self.press_d = True
                    elif event.key == K_w:
                        # Xử lý sự kiện nhấn phím "w"
                        self.press_w = True
                    elif event.key == K_SPACE:
                        pass
                if event.type == pygame.KEYUP:
                    if event.key == K_a:
                        # Xử lý sự kiện nhả phím "a"
                        self.press_a = False
                    elif event.key == K_s:
                        # Xử lý sự kiện nhả phím "s"
                        self.press_s = False
                    elif event.key == K_d:
                        # Xử lý sự kiện nhả phím "d"
                        self.press_d = False
                    elif event.key == K_w:
                        # Xử lý sự kiện nhả phím "w"
                        self.press_w = False
                    elif event.key == K_SPACE:
                        # Xử lý sự kiện nhấn phím "space"
                        if self.mBomber.status == Actor.ALIVE:
                            self.innitBomb()
                            self.mBomber.run_bomb = Actor.ALLOW_RUN

            self.draw()
            self.mBomber.draw_actor(self.screen)
            if self.other is not None:
                self.other.draw_actor(self.screen)

            self.move()
            self.set_run_bomber()
            self.check_impact_item()
            self.dead_line_all_bomb()
            self.check_dead()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def receive_response_from_server(self):
        while True:
            try:
                response = self.client_socket.recv(1024).decode()
                print("response:"+response)
                data = json.loads(response)

                # Kiểm tra phản hồi từ server
                if "END_GAME" in data:
                    with self.lock:
                        self.dialog_text = self.font.render("You Win", True, (255, 0, 0))
                        self.showDialog = True

                if "send_data" in data:
                    with self.lock:
                        self.other = Actor(data["x"], data["y"], data["type"], data["orient"], data["speed"],
                                           data["sizeBomb"],
                                           data["quantity_bomb"], data["img"], data["name"], data["heart"])
                if "send_data_item" in data:
                    with self.lock:
                        for item in self.arrItem:
                            if item.x == data["x"] and item.y == data["y"]:
                                self.arrItem.remove(item)
                                break
                if "send_bomb" in data:
                    with self.lock:
                        bomb = Bomb(data["x"], data["y"], data["size"], data["timeline"])
                        self.arrBomb.append(bomb)

            except json.JSONDecodeError as e:
                print("Error decoding JSON:", str(e))

    def send_data(self):
        if not self.is_sending_data:
            self.is_sending_data = True
            data = {
                "send_data": "send_data",
                "x": self.mBomber.x,
                "y": self.mBomber.y,
                "type": self.mBomber.type,
                "orient": self.mBomber.orient,
                "speed": self.mBomber.speed,
                "sizeBomb": self.mBomber.sizeBomb,
                "quantity_bomb": self.mBomber.quantity_bomb,
                "img": self.mBomber.img,
                "name": self.mBomber.name,
                "heart": self.mBomber.heart
            }

            self.client_socket.send(json.dumps(data).encode())
            self.is_sending_data = False

    def draw(self):
        self.screen.blit(self.main_Image, (0, 0))

        if self.drawMap:
            self.innit("../map1/BOX.txt", "../map1/ITEM.txt")
            self.drawMap = False

        self.drawAllItem()
        self.drawAllBox()

        # Dialog
        if self.showDialog:
            pygame.draw.rect(self.screen, (255, 255, 255), self.dialog_rect)  # Draw white background for dialog
            pygame.draw.rect(self.screen, (0, 0, 0), self.dialog_rect, 2)  # Draw black border for dialog
            self.screen.blit(self.dialog_text, (self.dialog_rect.x + 60, self.dialog_rect.y + 90))

    def move(self):
        if self.typeActor == 1:
            img = "bebong"
        else:
            img = "khokho"

        if not self.showDialog:
            if self.press_a:
                self.mBomber.changeOrient(Actor.LEFT, img + "_left", self.screen)
                self.mBomber.move(self.arrBomb, self.arrBox)
            elif self.press_d:
                self.mBomber.changeOrient(Actor.RIGHT, img + "_right", self.screen)
                self.mBomber.move(self.arrBomb, self.arrBox)
            elif self.press_s:
                self.mBomber.changeOrient(Actor.DOWN, img + "_down", self.screen)
                self.mBomber.move(self.arrBomb, self.arrBox)
            elif self.press_w:
                self.mBomber.changeOrient(Actor.UP, img + "_up", self.screen)
                self.mBomber.move(self.arrBomb, self.arrBox)
            self.send_data()

    def innit(self, pathBox, pathItem):
        self.arrBox = []
        self.arrBomb = []
        self.arrBombBang = []
        self.arrItem = []

        self.innitArrBox(pathBox)
        self.innitArrItem(pathItem)

    def innitArrItem(self, path):
        try:
            with open(path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    str = line.split(":")
                    x = int(str[0])
                    y = int(str[1])
                    type = int(str[2])
                    images = str[3].strip()
                    item = Item(x, y, type, images)
                    self.arrItem.append(item)
        except FileNotFoundError:
            traceback.print_exc()

    def innitArrBox(self, pathBox):
        try:
            with open(pathBox, 'r') as file:
                self.Background = file.readline().strip()
                lines = file.readlines()
                for line in lines:
                    str = line.split(":")
                    x = int(str[0])
                    y = int(str[1])
                    type = int(str[2])
                    images = str[3].strip()
                    box = Box(x, y, type, images)
                    self.arrBox.append(box)
        except FileNotFoundError:
            traceback.print_exc()

    # Đặt Bom
    def innitBomb(self):
        if self.mBomber.status == Actor.DEAD:
            return

        x = self.mBomber.x + self.mBomber.width // 2
        y = self.mBomber.y + self.mBomber.height // 2

        # kiểm tra bom mới có va chạm với các bom cũ hay không
        for bomb in self.arrBomb:
            if bomb.isImpact(x, y):
                return

        if len(self.arrBomb) >= self.mBomber.quantity_bomb:
            return

        mBomb = Bomb(x, y, self.mBomber.sizeBomb, 2.5)
        data = {
            "send_bomb": "send_bomb",
            "x": mBomb.x,
            "y": mBomb.y,
            "size": mBomb.size,
            "timeline": 2.5
        }

        self.client_socket.send(json.dumps(data).encode())
        self.arrBomb.append(mBomb)

    def drawAllItem(self):
        for item in self.arrItem:
            item.drawItem(self.screen)

    def drawAllBox(self):
        for box in self.arrBox:
            box.drawBox(self.screen)

    def check_impact_item(self):
        for index, item in enumerate(self.arrItem):
            if item.isImpactItemVsBomber(self.mBomber):
                if not self.is_sending_data:
                    self.is_sending_data = True

                    data = {
                        "send_data_item": "send_data_item",
                        "position": index,
                        "x": item.x,
                        "y": item.y
                    }

                    self.client_socket.send(json.dumps(data).encode())

                    self.is_sending_data = False
                if item.type == Item.Item_Bomb:
                    self.mBomber.quantity_bomb += 1
                    self.arrItem.remove(item)
                    break
                elif item.type == Item.Item_BombSize:
                    self.mBomber.sizeBomb += 1
                    self.arrItem.remove(item)
                    break
                elif item.type == Item.Item_Shoe:
                    self.mBomber.speed += 1
                    self.arrItem.remove(item)
                    break

    def set_run_bomber(self):
        if len(self.arrBomb) > 0:
            if not self.arrBomb[-1].setRun(self.mBomber):
                self.mBomber.set_run_bomb(Actor.DISALLOW_RUN)

    def dead_line_all_bomb(self):
        for i in range(len(self.arrBomb)):
            self.arrBomb[i].drawActor(self.screen)

        for i in range(len(self.arrBombBang)):
            self.arrBombBang[i].drawBongBang(self.screen)

        for i in range(len(self.arrBomb)):
            self.arrBomb[i].deadlineBomb()
            if self.arrBomb[i].timeline == 0:
                bom_bang = BombBang(self.arrBomb[i].x, self.arrBomb[i].y, self.arrBomb[i].size, self.arrBox)
                bom_bang.drawBongBang(self.screen)
                self.arrBombBang.append(bom_bang)
                self.arrBomb.pop(i)
                break

        # Kích nổ liên tục
        for i in range(len(self.arrBombBang)):
            for j in range(len(self.arrBomb)):
                if self.arrBombBang[i].isImpactBombBangvsBomb(self.arrBomb[j]):
                    bom_bang = BombBang(self.arrBomb[j].x, self.arrBomb[j].y, self.arrBomb[j].size,
                                        self.arrBox)
                    self.arrBombBang.append(bom_bang)
                    self.arrBomb.pop(j)
                    break

        for k in range(len(self.arrBombBang)):
            self.arrBombBang[k].deadlineBomb()

            if self.arrBombBang[k].timeLine == 0:
                for i in range(len(self.arrBombBang)):
                    if self.arrBombBang[i].isImpactBombBangVsActor(self.mBomber):
                        if self.mBomber.heart > 0:
                            self.mBomber.heart -= 1

                self.arrBombBang.pop(k)
                break

        for i in range(len(self.arrBombBang)):
            for j in range(len(self.arrBox)):
                if self.arrBombBang[i].isImpactBombBangvsBox(self.arrBox[j]):
                    self.arrBox.pop(j)
                    break

        for i in range(len(self.arrBombBang)):
            for j in range(len(self.arrItem)):
                if self.arrBombBang[i].isImpactBombBangvsItem(self.arrItem[j]):
                    self.arrItem.pop(j)
                    break

    def check_dead(self):
        if self.mBomber.heart == 0:
            if self.imgName == "bebong_down":
                self.mBomber.img = "bebong_dead"
            else:
                self.mBomber.img = "khokho_dead"

            self.mBomber.status = Actor.DEAD

            self.client_socket.send("END_GAME".encode())
            self.send_data()
            self.dialog_text = self.font.render("You Lose", True, (255, 0, 0))
            self.showDialog = True