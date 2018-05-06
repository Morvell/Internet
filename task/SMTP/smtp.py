# -*- coding: utf-8 -*-
import base64
import re
import socket
import ssl
import sys
import os


class SMTP:
    def __init__(self, server, port, rcpt_to, subject, fromName, toName, path, login=None,
                 password=None):
        self.server = server
        self.port = port
        self.login = login
        self.password = password
        self.rcpt_to = rcpt_to
        self.path = path
        self.subject = subject
        self.text = ""
        self.fromName = fromName
        self.toName = toName

    def make_ssl(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl_socket = ssl.wrap_socket(s)
        self.ssl_socket.settimeout(2.0)
        try:
            self.ssl_socket.connect((self.server, self.port))
            self.write_ans(self.ssl_socket)
            self.ehlo(self.ssl_socket)
        except Exception:
            print("\nWe can't connection to SMTP_SSL server\n")
            sys.exit()

    def get_images_base64(self):
        dict_images = dict()
        for f in os.listdir(self.path) :

            with open(self.path + "/" + f, "rb") as normal_file:
                try:
                    encoded_string = base64.standard_b64encode(
                        normal_file.read())
                    dict_images[f] = encoded_string
                except Exception:
                    print(
                        "\nSomething is wrong with file " + str(f) + "\n")
                    continue
        return dict_images

    def send_mail(self):
        try:
            self.make_ssl()
            self.auth(self.ssl_socket)
            self.make_mail(self.ssl_socket)
        except Exception:
            print("\nSomething is going wrong...\n")
            sys.exit()

    def auth(self, socket):
        socket.send(b"AUTH LOGIN\r\n")
        self.write_ans(socket)
        b64_login = base64.b64encode(self.login.encode())
        socket.send(b64_login + b"\r\n")
        self.write_ans(socket)
        b64_password = base64.b64encode(self.password.encode())
        socket.send(b64_password + b"\r\n")
        self.write_ans(socket)

    def make_mail(self, socket):
        rcpt_to_template = "rcpt to: <{0}>\r\n"
        command = "mail from: <{0}>".format(self.login) + "\r\n"
        command += rcpt_to_template.format(self.rcpt_to)
        command += "data\r\n"
        data = self.get_data().encode()
        socket.send(command.encode() + data)
        socket.send(b".\r\n")
        self.write_ans(socket)
        socket.send(b"quit\r\n")
        socket.close()

    def get_only_text(self):
        f = open('1.txt', encoding="utf-8")
        text = "\r\n"
        try:
            line = f.readline()
            while line:
                if re.match('^\.+.*', line):
                    text += '.' + line
                else:
                    text += line
                line = f.readline()
            f.close()
        except Exception as e:
            print(e)
        return text

    def get_data(self):
        start_template = "From: " + self.fromName +"<{0}>\r\n"
        to_template = "To: " + self.toName +"<{0}>\r\n".format(self.rcpt_to)

        message_template = ("Subject: " +
                            self.subject +
                            "\r\n"
                            "Content-Type: multipart/mixed; boundary=xyz\r\n"
                            "\r\n"
                            "--xyz\r\n"
                            "Content-Type: text/html; charset=utf-8\r\n"
                            "\r\n"
                            "<pre>" + self.get_only_text() + "</pre>\r\n"
                                                  "\r\n"
                                                  "--xyz\r\n")
        attachments = "attachments:\r\n"
        dict_images = self.get_images_base64()
        for f in dict_images:
            attachments += f + "\r\n"
        attachments += "\r\n"
        attachments += "--xyz\r\n"
        files_template = ""
        image_b64_template = ('Content-Type: image/{0}\r\n'
                              'Content-Disposition: attachment; filename="{1}"\r\n'
                              'Content-Transfer-Encoding: base64\r\n')
        counter = 0
        for f in dict_images:
            counter += 1
            if counter == len(dict_images):
                files_template += image_b64_template.format(
                    f[f.index(".") + 1:], f) + \
                                  "\r\n" + str(
                    dict_images[f].decode("UTF-8")) + "\r\n" + "--xyz--\r\n"
            else:
                files_template += image_b64_template.format(
                    f[f.index(".") + 1:], f) + \
                                  "\r\n" + str(
                    dict_images[f].decode("UTF-8")) + "\r\n" + "--xyz\r\n"
        final_template = start_template.format(self.login) + to_template + \
                         message_template + attachments + files_template
        return final_template

    def ehlo(self, s):
        try:
            s.send(b"EHLO Test\r\n")
            self.write_ans(s)
        except Exception:
            print("\nExept\n")
            sys.exit()

    def write_ans(self, s):
        ans = b""
        while True:
            try:
                temp = s.recv(1024)
                if temp:
                    ans += temp
            except Exception:
                break
        print("From server: " + ans.decode("UTF-8"))


def main():
    try:
        server = "smtp.yandex.ru"
        port = 465
        rcpt = "test270296@yandex.ru"
        subject = "SMTP (англ. Simple Mail Transfer Protocol — простой протокол передачи почты) — это широко используемый сетевой протокол, предназначенный для передачи электронной почты в сетях TCP/IP.  TP впервые был описан в RFC 821 (1982 год); последнее обновление в RFC 5321 (2008) включает масштабируемое расширение — ESMTP (англ.  Extended SMTP). В настоящее время под «протоколом SMTP», как правило, подразумевают и его расширения. Протокол SMTP предназначен для передачи исходящей почты с использованием порта TCP 25."
        path = "file"
        login = "test270296@yandex.ru"
        password = "27021996"
        fromName = "От Царя"
        toName = "Холопу"
        s = SMTP(server, port, rcpt, subject,fromName,toName, path, login, password)
        s.send_mail()
    except Exception:
        print("\nНе удалось отправить")
        sys.exit()


if __name__ == "__main__":
    main()
