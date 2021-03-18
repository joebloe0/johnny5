welcome to johnny proxy!

this is a way of accessing a proxy through a proxy

all you need is a proxy server you want to access and the proxy server you want to go through
these are labeled external and interal proxies respectively

options:
use_proxy (1,0): tells the proxy if it should go through in internal proxy
proxyip (string): this is the internal proxy, a valid option would be proxyip='127.0.0.1:3128'
ip (string): this is the ip to bind to when hosting the proxy, leave emptey to bind to all network adaptors (recommended)
port (integer): the port to bind to when hosting proxy
timeout (integer): the amount of time the proxy will wait for a socket to send data before terminating the connection
cacheexpire (integer): amount of seconds before a cache connection is terminated and a new connection is esablished
totalcache (interger): amount of cache connections to have open at the same time
enablecache(1,0): determines if cache connection should be established, setting this option to 0 will reduce speeds but only open connections on demand
external_proxy (string): the external proxy and ip, this can be a dns proxy too e.g. 'example.com:8080'
