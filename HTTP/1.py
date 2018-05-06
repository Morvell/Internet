import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("www.ugkp.ru",80))
    date = [b"TRACE * HTTP/1.1", b"HOST: www.ugkp.ru"]
    req = b'''\r\n'''.join(date)+b"\r\n\r\n"
    sock.send(req)
    print(sock.recv(1024).decode("cp1251"))
