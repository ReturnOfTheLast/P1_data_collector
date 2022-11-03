import socket
import json
from data_handler import handler

addr = ("192.168.4.50", 62222)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(addr)
print(f"Socket is bound on {addr[0]} port {addr[1]}")

while True:
    print("\nListening for data...")
    data = sock.recv(2048)
    print(f"Received: {data!r}")
    
    decoded_data = json.loads(data.decode("utf-8"))
    print(f"Decoded to: {decoded_data}")

    print("\nSending to data handler...")
    handler(decoded_data)
    print("Data handled")
