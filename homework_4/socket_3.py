import socket
import urllib.parse
from gpiozero import LED

red = LED(24)

IP = "192.168.1.177"

print(IP)
print(5001)
def run_socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, 5001))
    try:
        while True:
            data, address = sock.recvfrom(1024)

            data_parse = urllib.parse.unquote_plus(data.decode())

            if float(data_parse) > -0.5:
                red.on()
            else:
                red.off()
            
            

    except KeyboardInterrupt:
        print(f"Destroy server")
    finally:
        sock.close()


if __name__ == "__main__":
    run_socket_server()