import sys
import socket
import selectors
import types

class Client:
    selector = selectors.DefaultSelector()

    def __init__(self, host="127.0.0.1", port=7777):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex((host, port))
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(sock, events, data=data)

    def tick(self):
        events = self.selector.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                #what?
            else:
                self.service_connection(key, mask)
        

def start_connections(host, port, num_conns):
    print(f"Starting connection {connid} to {server_addr}")
    
    
    data = types.SimpleNamespace(
        connid=connid,
        msg_total=sum(len(m) for m in messages),
        recv_total=0,
        messages=messages.copy(),
        outb=b"",
    )
    

start_connections("127.0.0.1", 7777, 2)