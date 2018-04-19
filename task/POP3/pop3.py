import socket
import ssl

addr = ('pop.yandex.ru', 995)


def sendrecv(command, sock):
    sock.send((command + '\n').encode())
    return sock.recv(1024).decode()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock = ssl.wrap_socket(sock)
    sock.connect(addr)
    print(sock.recv(1024).decode())
    print(sendrecv('USER test270296', sock))
    print(sendrecv('PASS 27021996', sock))
    print(sendrecv('STAT', sock))
    print(sendrecv('LIST', sock))
    print(sendrecv('TOP 1 10', sock))
    print(sendrecv('RETR 1', sock))
    print(sendrecv('QUIT', sock))