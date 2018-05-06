import sys
import socket
import ssl
import traceback
from mail_parser import MailParser


class Pop3Client:
    def __init__(self, server, port, login, password, start, end):
        self.server = server
        self.port = port
        self.login = login
        self.password = password
        self.mails_count = None
        self.start = start
        self.end = end
        self.ssl_socket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.connect()
        self.auth()
        self.stat()

    def connect(self):
        try:
            self.ssl_socket.connect((self.server, self.port))
            ans = self.read().decode("UTF-8")
            if ans[:3] == "+OK":
                print("\nСоединение с сервером успешно\n")
            else:
                raise Exception
        except Exception:
            print("Сервер недоступен")
            sys.exit()

    def close_connection(self):
        self.ssl_socket.close()

    def auth(self):
        def send_and_check(data):
            self.ssl_socket.send(data.encode())
            ans = self.read().decode("UTF-8")
            if ans[:3] != "+OK":
                raise Exception

        try:
            send_and_check("USER " + self.login + "\r\n")
            send_and_check("PASS " + self.password + "\r\n")
        except Exception:
            print("\nВы ввели неправильный логин или пароль\n")
            sys.exit()
        print("\nЛогин и Пароль подошли\n")

    def stat(self):
        try:
            self.ssl_socket.send(b"STAT\r\n")
            ans = self.read().decode("UTF-8")
            self.mails_count = int(ans.split(" ")[1])
            print("\nВ Почтовом ящике {} Писем\n".format(self.mails_count))
        except Exception:
            print("\nНе удалось определить кол-во писем...\n")
            sys.exit()

    def get_mails(self):
        if self.mails_count < self.end:
            self.end = self.mails_count
        mail_parser = MailParser()
        for mail_index in range(self.start, self.end + 1, 1):
            try:
                a = self.try_to_read_mail(mail_index)
                yield mail_parser.parse(mail_index, a)
            except Exception:
                print("\nПроизошла ошибка в обработке {} письма\n".format(mail_index))
                continue
        self.close_connection()

    def read(self):
        return self.ssl_socket.recv(2**10)

    def try_to_read_mail(self, mail_index):
        def send_retr():
            self.ssl_socket.settimeout(0.25)
            self.ssl_socket.send("RETR {}\r\n".format(mail_index).encode())
            a = self.read().decode("UTF-8")
            if a[:3] == "+OK":
                return int(a.split(' ')[1]), a.encode()
            else:
                raise Exception

        def incorrect_answer(first_time):
            if first_time:
                print("Некорректный ответ сервера на письмо {}, пытаемся получить письмо заново".format(mail_index))
            clear_buffer()
                
        def clear_buffer():
            try:
                self.ssl_socket.settimeout(0.5)
                while True:
                    self.read()
            except Exception:
                return

        def read_mail(ans):
            while True:
                self.ssl_socket.settimeout(10)
                temp = self.ssl_socket.recv(2 ** 25)
                if temp:
                    ans += temp
                if len(str(ans)) >= size:
                    clear_buffer()
                    return ans

        ans = b""
        size = 0
        without_exception = True
        while size == 0:
            try:
                size, ans = send_retr()
            except Exception:
                try:
                    incorrect_answer(without_exception)
                    without_exception = False
                except Exception:
                    continue
        return read_mail(ans)