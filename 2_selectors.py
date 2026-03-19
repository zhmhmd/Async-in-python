import socket as socket1
import selectors


selector = selectors.DefaultSelector()


def server():
    server_socket = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
    server_socket.setsockopt(socket1.SOL_SOCKET, socket1.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()
    
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)
    
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)
        
        
def send_message(client_socket):
    
    request = client_socket.recv(4096)

    if request:
        response = 'Hello World!\n'.encode()
        client_socket.send(response)
    else:
        selector.unregister(client_socket)
        client_socket.close()
    

def event_loop():
    while True:
        
        events =selector.select()   # (key, events)
    
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)
        
    
if __name__ == '__main__':
    server()
    event_loop()