import socket
import threading
import os


class Server(threading.Thread):
    def __init__(self):
        super().__init__()
        self.host = "127.0.0.1"
        self.port = 55555
        self.connections = {}
        self.listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen.bind((self.host, self.port))
        self.listen.listen(5)
        print(f"Server listening at {self.listen.getsockname()}")

    def run(self):

        while True:
            client_socket, address = self.listen.accept()

            print(f"{address} has connected")

            client_messages = threading.Thread(
                target=self.handle_messages, args=(client_socket, address)
            )
            client_messages.start()

    def broadcast(self, msg, address, name=""):

        for connection in self.connections.values():
            connection.sendall(name.encode("ascii") + msg.encode("ascii"))

    def handle_messages(self, client_socket, address):

        client_socket.sendall(
            "Welcome to the chatroom, please type your name to continue".encode("ascii")
        )

        name = client_socket.recv(1024).decode("ascii")
        self.connections[name] = client_socket

        msg = f"{name} has just joined the chat."
        self.broadcast(msg, address)

        while True:

            try:
                message = client_socket.recv(1024).decode("ascii")
                if message:
                    if message == "QUIT":
                        quit = f"{name} has left the chat."
                        self.broadcast(quit, address)
                    else:
                        self.broadcast(message, address, name + ": ")
            except:
                print(f"client at {address} has closed the connection")
                client_socket.shutdown(socket.SHUT_RDWR)
                del self.connections[name]
                return


def exit(server):
    while True:
        ipt = input("")
        if ipt == "q":
            print("Closing all connections...")

            for connection in server.connections.values():
                connection.shutdown(socket.SHUT_RDWR)
            print("Shutting down the server...")
            os._exit(0)


server = Server()
server.start()
exit = threading.Thread(target=exit, args=(server,))
exit.start()
