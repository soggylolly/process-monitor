import socket

HOST = "192.168.99.223"   # VMs address from "ip addr"
PORT = 9999  # Match server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Same socket type as server

client.connect((HOST, PORT))  # connect() goes to server as opposed to waiting like server, Fails with ConnectionRefusedError if server isnt running yet

print("Connected. Type a message, or 'quit' to exit.")

with client:
    while True:
        message = input("> ")  # read line from keyboard

        if message == "quit":  # leaving loop closes socket
            break   # tells server we have gone

        client.sendall(message.encode())  # encode: text to bytes for sending
        reply = client.recv(1024)  # wait for echo
        print(f"Server said: {reply.decode()}")  # decode: bytes to text for reading