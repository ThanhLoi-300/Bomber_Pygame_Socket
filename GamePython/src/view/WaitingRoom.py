import json

import pygame
import socket
import threading
from src.view.EnterGame import EnterGame


class WaitingRoom:
    def __init__(self, screen, name, client_socket):
        pygame.init()
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.screen = screen
        self.name = name
        self.client_socket = client_socket
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.messages = []
        self.input_text = ''
        self.input_rect = pygame.Rect(10, self.HEIGHT - 40, self.WIDTH - 100, 30)
        self.send_button_rect = pygame.Rect(self.WIDTH - 80, self.HEIGHT - 40, 70, 30)
        self.client_sockets = []
        self.running = True
        self.lock = threading.Lock()
        self.server_full = False

        # Dialog hiển thị tên
        self.text = self.font.render("", True, (255, 0, 0))
        self.dialog_rect = pygame.Rect((self.WIDTH - 320), 20, 280, 200)
        self.dialog_text = self.text

        self.start_button_rect = pygame.Rect(self.WIDTH - 150, 300, 70, 30)

    def send_message(self, message):
        text = self.name + ": " + message
        data = {
            "send_message": text
        }
        self.client_socket.send(json.dumps(data).encode())

    def run(self):
        # Gửi request đến server
        self.client_socket.send("Get list user".encode())

        # Tạo một luồng riêng để nhận phản hồi từ máy chủ
        response_thread = threading.Thread(target=self.receive_response_from_server)
        response_thread.start()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.send_button_rect.collidepoint(mouse_pos):
                        if self.input_text:
                            self.send_message(self.input_text)
                            self.input_text = ''
                        else:
                            pass
                    elif self.start_button_rect.collidepoint(mouse_pos):
                        self.start_game()

            self.draw()

            if self.server_full:
                if self.name == self.client_sockets[0]:
                    actor = 1
                else:
                    actor = 2
                self.running = False
                EnterGame(self.screen, actor, self.name, self.client_socket).run()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def receive_response_from_server(self):
        while True:
            # Nhận phản hồi từ server
            response = self.client_socket.recv(1024).decode()
            # try:
            data = json.loads(response)
            print(data)

            # Kiểm tra phản hồi từ server
            if 'Get list user' in data:
                with self.lock:
                    self.client_sockets = data['Get list user'].split(', ')
            elif "receive_messages" in data:
                with self.lock:
                    self.messages.append(data["receive_messages"])
            elif "start_game" in data:
                with self.lock:
                    self.server_full = True
            #
            # except Exception as e:
            #     print("Lỗi đã xảy ra:", str(e))

    def draw(self):
        self.screen.fill((255, 255, 255))

        pygame.draw.rect(self.screen, (200, 200, 200), self.input_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.send_button_rect)

        if len(self.client_sockets) == 2 and self.name == self.client_sockets[0]:
            pygame.draw.rect(self.screen, (0, 0, 0), self.start_button_rect)

        input_text_surface = self.font.render(self.input_text, True, (0, 0, 0))
        self.screen.blit(input_text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        send_button_text = self.font.render("Send", True, (255, 255, 255))
        self.screen.blit(send_button_text, (self.send_button_rect.x + 10, self.send_button_rect.y + 8))

        start_button_text = self.font.render("Start", True, (255, 255, 255))
        self.screen.blit(start_button_text, (self.start_button_rect.x + 10, self.start_button_rect.y + 8))

        # Dialog
        pygame.draw.rect(self.screen, (255, 255, 255), self.dialog_rect)  # Draw white background for dialog
        pygame.draw.rect(self.screen, (0, 0, 0), self.dialog_rect, 2)  # Draw black border for dialog
        self.screen.blit(self.dialog_text, (self.dialog_rect.x + 15, self.dialog_rect.y + 75))

        messages_rect = pygame.Rect(20, 20, self.WIDTH - 340, self.HEIGHT - 150)
        pygame.draw.rect(self.screen, (220, 220, 220), messages_rect)

        message_y = messages_rect.y + 5
        for message in self.messages:
            message_surface = self.font.render(message, True, (0, 0, 0))
            self.screen.blit(message_surface, (messages_rect.x + 5, message_y))
            message_y += 25

        if len(self.client_sockets) > 0:
            text_name = f"User 1: {self.client_sockets[0]} and User 2: {self.client_sockets[1]}"
            self.text = self.font.render(text_name, True, (255, 0, 0))
            self.screen.blit(self.text, (self.dialog_rect.x + 15, self.dialog_rect.y + 75))
            text_name = "Me: " + self.name
            self.text = self.font.render(text_name, True, (255, 0, 0))
            self.screen.blit(self.text, (self.dialog_rect.x + 15, self.dialog_rect.y + 105))

            if len(self.messages) < 2:
                self.messages.append(self.client_sockets[0] + " đã tham gia")
                self.messages.append(self.client_sockets[1] + " đã tham gia")

    def start_game(self):
        self.client_socket.send("start_game".encode())
