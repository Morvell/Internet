import re


class Mail:
    def __init__(self, number, subject, from_who, size, to, date, message, attachments):
        self.number = number
        self.subject = subject
        self.from_who = from_who
        self.size = size
        self.to = to
        self.date = date
        self.message = message
        self.attachments = attachments

    def __str__(self):

        mess = self.message[0].replace("<div>","")
        mess = mess.replace("</div>","\n\r")

        s = "-----START_MAIL-----\n"
        s += "Number:     \t{}\nFrom:       \t{}\n".format(self.number, self.from_who)
        s += "To:         "
        j = True
        for i in self.to:
            if j:
                s += "\t{}\n".format(i.replace("\t", ""))
                j = False
            else:
                s += "            \t{}\n".format(i.replace("\t", ""))
        s += "Subject:    \t{}\nDate:       \t{}\nSize:       \t{} bytes\n".format(self.subject, self.date, self.size)
        s += "Message:\n\r\t{}\n".format(mess)
        s += "Attachments:\t"
        if len(self.attachments):
            i = 1
            for j in self.attachments:
                if i == 1:
                    s += "{}) {} ({} bytes)\n".format(i, j, self.attachments[j])
                    i += 1
                else:
                    s += " " * 12 + "\t{}) {} ({} bytes)\n".format(i, j, self.attachments[j])
        else:
            s += "No Attachments\n"
        s += "------END_MAIL------\n"
        return s
