import base64
import re
from email.header import decode_header
from email.parser import Parser
from email.policy import default

from mail import Mail
import email


def decode(data):
    dec = decode_header(data)
    encoding = dec[0][1]
    if encoding is None:
        encoding = "utf-8"
    ans = ""
    for j in range(len(dec)):
        if isinstance(dec[j][0], str):
            ans += dec[j][0]
        else:
            try:
                ans += dec[j][0].decode(encoding)
            except Exception:
                ans += dec[j][0].decode("Windows-1251")
    return ans


class MailParser:
    size_regexp = re.compile("\+OK\s(\d+)\s")
    attach_regexp = re.compile('Content-Disposition: attachment;\r\n\tfilename="(.*?)"', re.DOTALL)
    base_data = re.compile("\n([A-z0-9+/\n=\s]+)\n")
    data_to_encode = re.compile("^(=[?].+[?]=).*")
    field_regexp = re.compile("^([a-zA-Z-]+?):(.*)")
    message_regexp = re.compile("(<div>.*)\\n")

    def parse(self, number, data):
        try:
            dec_data = data.decode()
        except Exception:
            dec_data = data.decode("windows-1251")
        d = self.main_parse(dec_data)
        attachments = self.get_attachments(dec_data)
        try:
            return Mail(number, d["subject"], d["from"], d["size"], d["to"], d["date"], d["message"], attachments)
        except:
            raise


    def main_parse(self, data):
        d = dict()
        prev = None
        m = self.message_regexp.findall(data)
        for i in data.split("\r\n"):
            if i != "":
                a = self.field_regexp.findall(i)

                if len(a) > 0:
                    if a[0][0].lower() != "size":
                        d[a[0][0].lower()] = [a[0][1]]
                        prev = a[0][0].lower()
                elif prev is not None:
                    d[prev].append(i)
                else:
                    a = self.size_regexp.findall(i)
                    if len(a) > 0:
                        d["size"] = a[0]
        d["subject"] = self.decode_from_or_subject(d["subject"])
        d["from"] = self.decode_from_or_subject(d["from"])
        d["to"] = self.decode_to(d["to"])
        d["date"] = d["date"][0][1:]
        d["message"] = m
        return d

    def decode_to(self, data):
        ans = []
        for i in data:
            if " " in i:
                a = ""
                for j in i.split(" "):
                    if j != "":
                        if self.data_to_encode.match(j):
                            a += decode(j)
                        else:
                            a += j + " "
                ans.append(a)
            else:
                ans.append(decode(i))
        return ans

    def decode_from_or_subject(self, data):
        b = ""
        for i in data:
            b += i
        ans = ""
        for i in b.split(" "):
            i = i.replace('"', "").replace("\t", "")
            if i != "":
                if self.data_to_encode.match(i):
                    ans += decode(i)
                else:
                    ans += i + " "
        return ans

    def get_attachments(self, data):
        attachments = dict()
        for i in self.attach_regexp.findall(data):
            line = data[data.find(i):]
            s = self.base_data.findall(line)[0]
            try:
                f = open(i, 'wb+')
            except Exception as e:
                print(e)

            for line in s.split("\r\n"):
                f.write(base64.b64decode(line))
            attachments[decode(i)] = str((len(s) * 6) // 8) + " bytes"
        return attachments
