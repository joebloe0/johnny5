version = 1
features = ''
import socket
import socketserver
import time
import threading
import requests
enabled = 1
total = []
cache = []
f = open('options.txt', 'r')
lines = f.readlines()
f.close()
serverip = lines[0].strip()
proxy = serverip.split('=')[1]
proxy = int(proxy)
serverip = lines[1].strip()
serverip = serverip.split("='")[1].strip("'").split(":")
proxyip = (serverip[0], int(serverip[1]))
serverip = lines[2].strip()
x = str(serverip.split("='")[1].strip("'"))
serverip = lines[3].strip()
y = int(serverip.split('=')[1])
serverip = lines[4].strip()
timeout = float(serverip.split('=')[1])
serverip = lines[5].strip()
cacheexpire = float(serverip.split('=')[1])
serverip = lines[6].strip()
amountofcache = int(serverip.split('=')[1])
serverip = lines[7].strip()
cacheenable = int(serverip.split('=')[1])
serverip = lines[8].strip()
external_proxy = str(serverip.split("='")[1].strip("'"))
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global total
        global enabled
        global proxy
        global external_proxy
        global cache
        if enabled:
            cur_thread = threading.current_thread()
            total.append(str(cur_thread))
            if len(cache) <= 1:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if proxy:
                    sock.connect(proxyip)
                    sock.send(
                        b'CONNECT ' + external_proxy.encode() + b' HTTP/1.1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0\r\nProxy-Connection: keep-alive\r\nConnection: keep-alive\r\nHost: ' + external_proxy.encode() + b'\r\n\r\n')
                    sock.recv(1024 * 1024)
                else:
                    sock.connect(
                        (socket.gethostbyname(external_proxy.split(':')[0]), int(external_proxy.split(':')[1])))
            else:
                sock = cache[0][1]
                cache.remove(cache[0])
            if 1:
                lastrecv = time.time()
                self.request.setblocking(0)
                sock.setblocking(0)
                reader1 = self.request.makefile('rb', 1)
                writer1 = self.request.makefile('wb', 1)
                reader2 = sock.makefile('rb', 1)
                writer2 = sock.makefile('wb', 1)

                while True:
                    sec = time.time()
                    try:
                        data = reader1.read()
                        if not data is None:
                            try:

                                writer2.write(data)
                                lastrecv = sec
                            except:
                                break
                            if data == b'': break
                    except:
                        pass

                    try:
                        data = reader2.read()
                        if not data == None:
                            try:
                                writer1.write(data)
                                lastrecv = sec
                            except:
                                break
                            if data == b'': break
                    except:
                        pass

                    if sec - lastrecv > timeout: break
                    time.sleep(0.0001)
                total.remove(str(cur_thread))
                sock.close()
                # print("closed connection " + str(cur_thread))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = x, y

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        ip, port = server.server_address
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        #print("Server loop running in thread:", server_thread.name)
        last = 0
        proxies = {
            "https": "http://127.0.0.1:" + str(y),
        }
        try:
            x = requests.get("https://raw.githubusercontent.com/joebloe0/johnny5/main/source.py", proxies=proxies)
            print('proxy connection established successfully')
            new = int(x.text.split('\n')[0].split('version = ')[1])
            new = 3
            if new > version:
                print('NEWER VERSION AVAILABLE! please goto https://github.com/joebloe0/johnny5/releases to download the newest version')
                print(eval(x.text.split('\n')[1].split('features = ')[1]))
                print('running program in 15 seconds...')
                enabled = 0
                time.sleep(15)
                print('running...')
                enabled = 1

        except:
            pass
        while True:


            while len(cache) < amountofcache:
                #print("create")
                sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if proxy:
                    sock1.connect(proxyip)
                    sock1.send(b'CONNECT ' + external_proxy.encode() + b' HTTP/1.1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0\r\nProxy-Connection: keep-alive\r\nConnection: keep-alive\r\nHost: ' + external_proxy.encode() + b'\r\n\r\n')
                    sock1.recv(1024 * 1024 * 10)
                    # print(sock.recv(1024 * 1024 * 10))


                else:
                    sock1.connect((socket.gethostbyname(external_proxy.split(':')[0]), int(external_proxy.split(':')[1])))
                    cache.append([time.time(), sock1])
                #print("complete")
            for x in cache:
                if time.time() - x[0] >= cacheexpire:
                    #print("closing expired cache socket")
                    x[1].close()
                    cache.remove(x)
                    #print("closed expired cache socket")
            #print(x)
            #print(len(cache))

            time.sleep(0.05)
