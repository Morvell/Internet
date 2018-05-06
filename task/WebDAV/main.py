import base64
import socket
import ssl
import hashlib


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def sha256(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


with socket.socket() as sock:
    sock = ssl.wrap_socket(sock)
    sock.connect(('webdav.yandex.ru', 443))
    f = open("1.jpg", 'rb')
    file = f.read()
    data = [b"PUT /img.png HTTP/1.1",
            b"HOST: webdav.yandex.ru",
            b"Accept: */*",
            b"Authorization: Basic " + base64.b64encode(b"test270296:27021996"),
            b'Etag: ' + md5('1.jpg').encode(),
            b'Sha256: ' + sha256('1.jpg').encode(),
            b'Expect: 100-continue',
            b'Content-Type: application/binary',
            b'Content-Length: ' + str(len(file)).encode(),
            b'\r\n']
    req = b'\r\n'.join(data)
    print(req.decode())
    print()
    sock.send(req)
    print(sock.recv(6000).decode())
    sock.send(file)
    print(sock.recv(6000).decode())