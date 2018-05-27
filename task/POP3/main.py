import configparser

from pop3_client import Pop3Client


def main():
    config = configparser.ConfigParser()
    config.sections()
    config.read('example.ini')
    pop_server = config.get("DEFAULT","pop_server")
    port = config.getint("DEFAULT","port")
    login = config.get("DEFAULT","login")
    password = config.get("DEFAULT","password")
    start = config.getint("DEFAULT","start")
    end = config.getint("DEFAULT","end")


    for mail in Pop3Client(pop_server, port, login, password, start, end).get_mails():
        print(mail)

if __name__ == "__main__":
    main()