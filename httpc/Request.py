import socket
from urllib.parse import urlparse


class Request:

    """" This is a request object builder """

    method = ""
    host = ""
    port = 80
    path = ""
    headers = None
    queries = None
    data = None
    sock = socket

    def __init__(self, method, headers, data, url):
        self.method = method
        self.host = ""
        self.headers = headers

        if data is not None:
            self.data = data

        self.url_extract(url)
        self.sock = socket
        self.host_ip = None
        self.set_socket()

        print(headers)

    def to_string(self):

        temp_str = self.method + " " + self.path
        print(self.path)
        if self.queries:
            temp_str = temp_str + "?" + self.queries

        if temp_str[-1] != " ":
            temp_str = temp_str + " "

            temp_str = temp_str + "HTTP/1.1\r\n"
            temp_str = temp_str + "Host: " + self.host + ":" + str(self.port) + "\r\n"

        if self.headers is not None:
            for header in self.headers:
                if len(header) == 2:
                    temp_str = temp_str + header[0]+":"+header[1] + "\r\n"

        if self.method == "POST":
            temp_str += "Content-Length:"+str(len(self.data)) + "\r\n"

        temp_str = temp_str + "\r\n"

        if self.data is not None:
            temp_str += self.data
        return temp_str

    def encode_request(self):
        return self.to_string().encode()

    def url_extract(self, url):
        pu = urlparse(url)
        if pu.scheme != 'http' and pu.scheme != 'https':
            if url[0] is not '/' and url[1] is not '/':
                url = "//" + url

        pu = urlparse(url)
        self.host = pu.netloc

        if pu.port is not None:
            self.port = pu.port

        self.path = pu.path
        self.queries = pu.query

    def set_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("socket creation failed with error %s" % (err))

        try:
            self.host_ip = socket.gethostbyname(self.host)
        except socket.gaierror:
            print("there was an error resolving the host")

    def send_req(self):
        self.sock.connect((self.host, self.port))
        self.sock.sendall(self.encode_request())
        response = self.sock.recv(4096)
        response = response.decode()

        parsed_resp = response.split("\r\n\r\n")
        status = parsed_resp[0].split(" ")[1]

        if int(status) >= 300 and int(status) < 400:
            print("redirect status")

        return response
