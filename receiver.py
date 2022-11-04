# Import Modules
import socket
import json
import logging
from concurrent.futures import  ThreadPoolExecutor
from dblibs import handler

# Define logging behavior
log_format = "%(asctime)s %(levelname)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")

# Let the scanner know what your ip is
neg_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scanner_up = False
while not scanner_up:
    try:
        neg_sock.connect("192.168.4.100", 61111)
        if neg_sock.recv(512) == b"\x01":
            scanner_up = True
    except:
        pass

neg_sock.close()


# Define bind address
addr = ("", 62222)

# Make socket and bind it to the address
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(addr)
logging.info(f"Socket is bound on {addr[0]} port {addr[1]}")

# Make thread function for handler
def handler_thread(name, data):
    logging.info(f"Handler {name} starting")
    decoded_data = json.loads(data.decode("utf-8"))
    handler(name, decoded_data)
    logging.info(f"Handler {name} finishing")

# Make a thread pool with 4 threads
threadpool = ThreadPoolExecutor(max_workers=4)

# Count the Frames
frame_number = 0

# Main Loop
while True:
    try:
        logging.info(f"Listening for data frame {frame_number}")
        data = sock.recv(2048)
        logging.info(f"Received data frame {frame_number}")
        logging.info(f"{data!r}")
        # Submit handler to thread pool
        threadpool.submit(handler_thread, frame_number, data)
        frame_number += 1
    except KeyboardInterrupt:
        break

threadpool.shutdown(wait=True)
