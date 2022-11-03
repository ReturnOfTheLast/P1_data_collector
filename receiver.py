# Import Modules
import socket
import json
import logging
import threading
from dblibs import handler

# Define logging behavior
log_format = "%(asctime)s %(levelname)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")

# Define bind address
addr = ("192.168.4.50", 62222)

# Make socket and bind it to the address
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(addr)
logging.info(f"Socket is bound on {addr[0]} port {addr[1]}")

# Make thread function for handler
def handler_thread(name, data):
    logging.info(f"Handler {name} starting")
    decoded_data = json.loads(data.decode("utf-8"))
    handler(decoded_data)
    logging.info(f"Handler {name} finishing")

frame_number = 0

# Main Loop
while True:
    logging.info(f"Listening for data frame {frame_number}")
    data = sock.recv(2048)
    logging.info(f"Received data frame {frame_number}")
    logging.info(f"{data!r}")
    t = threading.Thread(target=handler_thread, args=(frame_number, data))
    t.start()
    frame_number += 1
