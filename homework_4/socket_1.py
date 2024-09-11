import socket
import urllib.parse


IP = socket.gethostname()

print(IP)

def run_socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, 5000))
    try:
        while True:
            data = sock.recvfrom(1024)


            sock.sendto(data[0], ("192.168.1.177", 5001))



    except KeyboardInterrupt:
        print(f"Destroy server")
    finally:
        sock.close()


if __name__ == "__main__":
    run_socket_server()