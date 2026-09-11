import socket

HOST = "127.0.0.1"  # loops back to this machine only
PORT = 9999  # Port chosen thats unlikely to clash

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket using IPv4 addresses and TCP

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # without this restarting server gives "Address already in use" as OS holds port for a minute after close

server.bind((HOST, PORT))  # claim this address and port
server.listen(1)  # how many connections may queue

print(f"Listening on {HOST}:{PORT}")

conn, addr = server.accept()  # accept() blocks until client connects, returns a new socket for client through conn plus clients addres
print(f"Connected by {addr}")

with conn:  # closes conn automatically when block ends
    while True:
        data = conn.recv(1024)  # wait for up to 1024 bytes (Also blocks)

        if not data:  # If bytes are empty the client closed the connection
            print("Client disconnected")
            break

        print(f"Received: {data.decode()}")  # decode: bytes to text in order to print
        conn.sendall(data)  # send the raw bytes straight back