from pop3_client import Pop3Client


def main():
    pop_server = "pop.yandex.ru"
    port = 995
    login = "test270296"
    password = "27021996"
    start = 1
    end = 1

    for mail in Pop3Client(pop_server, port, login, password, start, end).get_mails():
        print(mail)

if __name__ == "__main__":
    main()