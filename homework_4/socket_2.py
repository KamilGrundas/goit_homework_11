import socket


IP = "car"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"3.1", (IP, 5000))