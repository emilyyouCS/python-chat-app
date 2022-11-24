import os
import socket
import threading
import tkinter as tk


class Client(threading.Thread):
    def __init__(self):
        super().__init__()
        self.host = "127.0.0.1"
        self.port = 55555
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messages = None

    def start(self):

        self.sock.connect((self.host, self.port))
        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.start()

    def send(self, text_input):

        message = text_input.get()
        text_input.delete(0, tk.END)

        if message == "QUIT":
            self.sock.sendall("QUIT".encode("ascii"))
            self.sock.close()
            os._exit(0)

        else:
            self.sock.sendall(message.encode("ascii"))

    def receive_message(self):

        while True:
            message = self.sock.recv(1024).decode("ascii")

            if message:
                if self.messages:
                    self.messages.insert(tk.END, message)
            else:
                print("\nOh no, we have lost connection to the server!")
                print("\nQuitting...")
                self.sock.shutdown(socket.SHUT_RDWR)
                os._exit(0)


def main():
    client = Client()

    window = tk.Tk()
    window.title("Chatroom")

    frm_messages = tk.Frame(master=window)
    scrollbar = tk.Scrollbar(master=frm_messages)

    messages = tk.Listbox(master=frm_messages, yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frm_messages.grid(row=0, column=0, columnspan=2, sticky="nsew")
    frm_entry = tk.Frame(master=window)

    text_input = tk.Entry(master=frm_entry)
    text_input.pack(fill=tk.BOTH, expand=True)

    text_input.bind("<Return>", lambda x: client.send(text_input))
    text_input.insert(0, "Enter your username to begin")

    btn_send = tk.Button(
        master=window, text="Send", command=lambda: client.send(text_input)
    )

    frm_entry.grid(row=1, column=0, padx=10, sticky="ew")
    btn_send.grid(row=1, column=1, pady=10, sticky="ew")

    window.rowconfigure(0, minsize=500, weight=1)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure(0, minsize=500, weight=1)
    window.columnconfigure(1, minsize=200, weight=0)

    client.start()
    client.messages = messages

    window.mainloop()


main()
