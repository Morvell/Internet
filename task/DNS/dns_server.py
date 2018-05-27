import socket
import time

import dnslib


class DnsServer:
    def __init__(self, forwarder, forwarder_port):
        self.cache = dict()
        self.forwarder = forwarder
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_sock.bind(("127.0.0.1", 53))
        self.forwarder_port = forwarder_port

    def put_in_cache(self, query):
        self.cache.update(
            {str(query.q.qname) + str(query.q.qtype): (time.time()+query.a.ttl ,dnslib.DNSRecord(rr=query.rr))})
        if len(query.auth) != 0:
            self.cache.update({str(query.auth[0].rname) +
                               str(query.auth[0].rtype): (time.time() + query.auth[0].ttl,dnslib.DNSRecord(rr=query.auth))})
        if len(query.ar) != 0:
            for ar in query.ar:
                nil = list()
                nil.append(ar)
                self.cache.update(
                    {str(ar.rname) + str(ar.rtype): (time.time()+ar.ttl, dnslib.DNSRecord(rr=nil))})

    def make_RRs(self,rrs,end_time):
        nil = list()
        for rr in rrs:
            nil.append(dnslib.RR(rr.rname,rr.rtype,rr.rclass,int(end_time - time.time()),rr.rdata))
        return nil

    def run(self):
        while True:
            try:
                full_query, fromaddr = self.client_sock.recvfrom(1024)
                query = dnslib.DNSRecord.parse(full_query)

                print(str(query.header.q))
                if str(query.q.qname)+str(query.q.qtype) in self.cache:
                    from_cache_tuple = self.cache.get(str(query.q.qname)+str(query.q.qtype))

                    print("осталось жить пакету" + str(from_cache_tuple[0] - time.time()))

                    if from_cache_tuple[0] < time.time():
                        self.update_cache(full_query,fromaddr)
                    else:
                        from_cache = from_cache_tuple[1]
                        header = dnslib.DNSHeader(id=query.header.id,
                                                  q=from_cache.header.q,
                                                  )
                        new_answer = dnslib.DNSRecord(header,
                                                      query.questions,
                                                      self.make_RRs(
                                                          from_cache.rr,
                                                          from_cache_tuple[0]))
                        answer1 = new_answer.pack()
                        self.client_sock.sendto(answer1, fromaddr)
                        print("from cache")
                else:
                    self.update_cache(full_query,fromaddr)

            except socket.timeout:
                print("Что-то явно не так")
                continue

    def update_cache(self, full_query, fromaddr):
        answer = self.ask_forwarder(full_query)
        self.client_sock.sendto(answer.pack(), fromaddr)
        self.put_in_cache(answer)
        print("cache update")

    def ask_forwarder(self, full_query):
        with socket.socket(socket.AF_INET,
                           socket.SOCK_DGRAM) as forwsock:
            try:
                forwsock.connect((self.forwarder, 53))
                forwsock.sendto(full_query, (self.forwarder, 53))
                forwsock.settimeout(3)
                data, addr = forwsock.recvfrom(1024)
                return dnslib.DNSRecord.parse(data)

            except socket.timeout:
                print("Сервер чет не отвечает")
            except Exception as e:
                print("Что-то пошло не так")


def main():
    forwarders = ['8.8.8.8', '195.93.187.26', '8.8.4.4']
    forw_id = 1
    forwarder = forwarders[forw_id]
    port = 53

    DnsServer(forwarder, port).run()


if __name__ == '__main__':
    main()
