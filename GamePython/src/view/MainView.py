
import pygame
from pygame.locals import *

from src.view.EnterGame import EnterGame
from src.view.WaitingRoom import WaitingRoom

import socket
import threading

HOST = '192.168.51.242'  # Địa chỉ IP của máy chủ
PORT = 8080  # Số cổng để kết nối

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


class MainView:
    WIDTHJF = 750
    HEIGHTJF = 675

    def __init__(self):
        pygame.init()
        self.running = True
        self.lock = threading.Lock()
        self.server_full = False
        self.name = ""
        self.view = pygame.display.set_mode((self.WIDTHJF, self.HEIGHTJF))
        pygame.display.set_caption("Easy BOOM!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)  # Font cho văn bản đầu vào

        # Load image
        icon_image = pygame.image.load("../Images/dau.png")  # Path to your icon image
        icon_image = pygame.transform.scale(icon_image, (32, 32))
        self.main_Image = pygame.image.load("../Images/background_Menu.png")
        self.main_Image = pygame.transform.scale(self.main_Image, (
            self.WIDTHJF, self.HEIGHTJF))  # Chia tỷ lệ hình ảnh để phù hợp với màn hình

        self.button_start_image = pygame.image.load("../Images/Play.png")  # Load the image for the button
        self.button_start_image = pygame.transform.scale(self.button_start_image, (300, 100))  # Scale the button image
        self.button_start_hover = pygame.image.load("../Images/Play2.png")
        self.button_start_hover = pygame.transform.scale(self.button_start_hover, (300, 100))  # Scale the button image

        # Calculate center position
        icon_size = icon_image.get_size()
        icon_x = (32 - icon_size[0]) // 2  # Center horizontally
        icon_y = (32 - icon_size[1]) // 2  # Center vertically

        # Create a Surface for icon
        self.icon_surface = pygame.Surface((32, 32))
        self.icon_surface.fill((255, 255, 255))
        self.icon_surface.blit(icon_image, (icon_x, icon_y))  # Draw the image at center
        pygame.display.set_icon(self.icon_surface)  # Set the surface as icon

        # Create a start button
        button_width, button_height = self.button_start_image.get_size()
        self.start_button = pygame.Rect((self.WIDTHJF - button_width) // 2, (self.HEIGHTJF - 150), button_width,
                                        button_height)

        self.button_state = 'normal'  # Initial state of the button

        # Input box
        self.input_rect = pygame.Rect((self.WIDTHJF - 250) // 2, (self.HEIGHTJF - 200), 260,
                                      40)  # Vị trí và kích thước của ô đầu vào
        self.input_text = ''  # Chuỗi văn bản nhập vào

        # Dialog
        self.mess = self.font.render("Name is not empty", True, (255, 0, 0))
        self.dialog_rect = pygame.Rect((self.WIDTHJF - 300) // 2, (self.HEIGHTJF - 200) // 2, 300, 200)
        self.dialog_text = self.mess
        self.show_dialog = False

        pygame.display.flip()

    def run(self):
        # Tạo một luồng riêng để nhận phản hồi từ máy chủ
        response_thread = threading.Thread(target=self.receive_response_from_server)
        response_thread.start()
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == K_RETURN:  # Set event when press enter
                        if self.input_text.strip() == '':
                            self.mess = self.font.render("Name is not empty", True, (255, 0, 0))
                            self.dialog_text = self.mess
                            self.show_dialog = True
                            pygame.time.set_timer(USEREVENT, 2000)
                        else:
                            # Gửi tên đến server
                            client_socket.send(self.input_text.encode())
                            self.name = self.input_text
                    else:
                        self.input_text += event.unicode
                elif event.type == MOUSEMOTION:  # Handle mouse motion event
                    if self.start_button.collidepoint(event.pos):  # If the mouse is over the button
                        self.button_state = 'hover'
                    else:
                        self.button_state = 'normal'
                elif event.type == MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        if self.input_text.strip() == '':
                            self.mess = self.font.render("Name is not empty", True, (255, 0, 0))
                            self.dialog_text = self.mess
                            self.show_dialog = True
                            pygame.time.set_timer(USEREVENT, 2000)
                        else:
                            # Gửi tên đến server
                            client_socket.send(self.input_text.encode())
                            self.name = self.input_text

                elif event.type == USEREVENT:
                    self.show_dialog = False

            # Draw everything
            self.view.blit(self.icon_surface, (0, 0))  # Draw the main_Image
            self.view.blit(self.main_Image, (0, 0))  # Draw the main_Image
            self.view.blit(self.button_start_image, self.start_button)

            # Draw input box
            pygame.draw.rect(self.view, (255, 255, 255), self.input_rect)
            pygame.draw.rect(self.view, (0, 0, 0), self.input_rect, 2)
            text_surface = self.font.render(self.input_text, True, (0, 0, 0))
            self.view.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 10))

            if self.button_state == 'normal':
                self.view.blit(self.button_start_image,
                               self.start_button)  # Draw the normal state button image on the screen
            elif self.button_state == 'hover':
                self.view.blit(self.button_start_hover,
                               self.start_button)  # Draw the hover state button image on the screen

            # Draw dialog if needed
            if self.show_dialog:
                pygame.draw.rect(self.view, (255, 255, 255), self.dialog_rect)  # Draw white background for dialog
                pygame.draw.rect(self.view, (0, 0, 0), self.dialog_rect, 2)  # Draw black border for dialog
                self.view.blit(self.dialog_text, (self.dialog_rect.x + 25, self.dialog_rect.y + 75))

            if self.server_full:
                self.running = False  # Dừng vòng lặp chính
                waiting_room = WaitingRoom(self.view, self.name, client_socket)
                waiting_room.run()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    def receive_response_from_server(self):
        while True:
            # Nhận phản hồi từ server
            response = client_socket.recv(1024).decode()

            # Kiểm tra phản hồi từ server
            if response == "EXIST":
                self.mess = self.font.render("Name is existed", True, (255, 0, 0))
                self.dialog_text = self.mess
                self.show_dialog = True
                pygame.time.set_timer(USEREVENT, 2000)
            elif response == "SERVER_FULL":
                with self.lock:
                    self.server_full = True
                break
            elif response == "OK":
                self.mess = self.font.render("Waiting for other user", True, (255, 0, 0))
                self.dialog_text = self.mess
                self.show_dialog = True


if __name__ == '__main__':
    game = MainView()
    game.run()
