import sys
import socket
import selectors
import types

class Server:
    selector = selectors.DefaultSelector()

    def __init__(self, host="127.0.0.1", port=7777):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen()
        print("Server running on", host, ":", port)
        sock.setblocking(False)
        self.selector.register(sock, selectors.EVENT_READ, data=None)

    def connect(self, sock):
        connection, address = sock.accept()
        print(address, "connected")
        connection.setblocking(False)
        data = types.SimpleNamespace(address=address, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(connection, events, data=data)

    def get_data(key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                print(recv_data, "recieved")
                data.outb += recv_data
            else:
                print(data.address, "disconnected")
                self.selector.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print(f"Echoing {data.outb!r} to {data.addr}")
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
    
    def tick(self):
        events = self.selector.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                self.accept_wrapper(key.fileobj)
            else:
                self.service_connection(key, mask)

