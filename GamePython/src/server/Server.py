import json
import socket
import threading


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sockets = {}
        self.running = False
        self.lock = threading.Lock()

    def start(self):
        self.server_socket.bind(('192.168.51.242', 8080))
        self.server_socket.listen()
        print('Waiting for connections...')
        self.running = True

        while self.running:
            client_socket, address = self.server_socket.accept()

            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while self.running:
            try:
                request = client_socket.recv(1024).decode()
                print(request)

                if "send_data_item" in request:
                    request = json.loads(request)
                    data = {
                        "send_data_item": request["send_data_item"],
                        "position": request["position"],
                        "x": request["x"],
                        "y": request["y"]
                    }
                    json_data = json.dumps(data)
                    for client in self.client_sockets.values():
                        if client != client_socket:
                         client.send(json_data.encode())

                if "send_bomb" in request:
                    request = json.loads(request)
                    data = {
                        "send_bomb": request["send_bomb"],
                        "x": request["x"],
                        "y": request["y"],
                        "size": request["size"],
                        "timeline": request["timeline"]
                    }
                    json_data = json.dumps(data)
                    for client in self.client_sockets.values():
                        if client != client_socket:
                            client.send(json_data.encode())

                if request == "start_game":
                    data = {
                        "start_game": "start_game"
                    }

                    json_data = json.dumps(data)
                    for client in self.client_sockets.values():
                        client.send(json_data.encode())

                if request == "END_GAME":
                    data = {
                        "END_GAME": "END_GAME"
                    }
                    json_data = json.dumps(data)
                    for client in self.client_sockets.values():
                        if client != client_socket:
                            client.send(json_data.encode())

                if request == "Get list user":
                    user_list = ", ".join(self.client_sockets.keys())
                    data = {
                        "Get list user": user_list
                    }

                    json_data = json.dumps(data)
                    client_socket.send(json_data.encode())

                if len(self.client_sockets) < 2:
                    if len(request) != 0:
                        # Kiểm tra tên trong client_sockets
                        if request in self.client_sockets:
                            # Gửi phản hồi "EXIST" nếu tên đã tồn tại
                            client_socket.send("EXIST".encode())
                            # client_socket.close()
                            continue
                        else:
                            with self.lock:
                                # Gửi phản hồi "OK" nếu tên chưa tồn tại
                                client_socket.send("OK".encode())
                                # Thêm key là name và value là client_socket vào client_sockets
                                if len(self.client_sockets) < 2:
                                    self.client_sockets[request] = client_socket

                                # print('user hiện tại: ', self.client_sockets)

                    if len(self.client_sockets) == 2:
                        for client in self.client_sockets.values():
                            client.send("SERVER_FULL".encode())

                if "send_message" in request:
                    request = json.loads(request)
                    data = {
                        "receive_messages": request["send_message"]
                    }

                    for client in self.client_sockets.values():
                        client.send(json.dumps(data).encode())

                if "send_data" in request:
                    request = json.loads(request)
                    data = {
                        "send_data": request["send_data"],
                        "x": request["x"],
                        "y": request["y"],
                        "type": request["type"],
                        "orient": request["orient"],
                        "speed": request["speed"],
                        "sizeBomb": request["sizeBomb"],
                        "quantity_bomb": request["quantity_bomb"],
                        "img": request["img"],
                        "name": request["name"],
                        "heart": request["heart"]
                    }

                    json_data = json.dumps(data)
                    for client in self.client_sockets.values():
                        if client != client_socket:
                            client.send(json_data.encode())

            except:
                # Mất kết nối từ client
                # for name, socket in self.client_sockets.items():
                #     if socket == client_socket:
                #         self.client_sockets.pop(name)
                #         break
                pass

    def stop(self):
        self.running = False
        self.server_socket.close()


if __name__ == '__main__':
    server = Server()
    server.start()
