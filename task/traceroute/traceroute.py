import socket
import configparser
from json import loads
from urllib.request import urlopen


def trace(destination_ip, hops, timeout):
    print(dest_ip)
    ttl = 1
    ip = None

    while ip != destination_ip and ttl != hops:

        ip = start_trace(dest_ip, ttl, timeout)

        if ip == 'timeout':
            print("{}.\t{}\tВремя ожидания истекло".format(ttl, "***"))

        elif is_white_ip(ip):
            print("{}.\t{}\t{}".format(ttl, ip, get_as_inf(ip)))

        ttl += 1


def start_trace(dest_ip, ttl, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    sock.settimeout(timeout)
    sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    icmp_echo = b'\x08\x00\xb5\xbc\x42\x42\x00\x01'

    try:
        sock.sendto(icmp_echo, (dest_ip, 43))
        _, ip = sock.recvfrom(1024)
        addr = ip[0]
        return addr
    except socket.timeout:
        return 'timeout'
    except:
        print("Интеернет тютю")
        exit()
    finally:
        sock.close()


def is_white_ip(ip):
    noneWhite = {
        ('10.0.0.0', '10.255.255.255'),
        ('172.16.0.0', '172.31.255.255'),
        ('192.168.0.0', '192.168.255.255'),
        ('127.0.0.0', '127.255.255.255')}

    for noneWhiteIp in noneWhite:
        if noneWhiteIp[0] <= ip <= noneWhiteIp[1]:
            return False
    return True


def get_as_inf(ip):
    info = loads(urlopen(f'http://ipinfo.io/{ip}/json').read())
    keys = ["country", "region", "city", "org"]
    message = ""
    for key in keys:
        if key in info:
            message += '{} '.format(info[key])
        else:
            message += 'информация не достуна - {},'.format(key.upper())
    return message


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")

    dest_ip = config.get("Destination", "Destination")
    ttl = config.getint("TTL", "TTL")
    timeout = config.getint("Timeout", "Timeout")

    try:
        trace(socket.gethostbyname(dest_ip), ttl, timeout)
    except:
        print("Инетренет ")
