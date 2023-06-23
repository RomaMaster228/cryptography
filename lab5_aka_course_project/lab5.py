import socket
import ssl
import time
import datetime

context = ssl.SSLContext()
context.options |= ssl.OP_NO_TICKET
context.verify_mode = ssl.CERT_NONE # disable cert. validation
dn = "mai.ru" # example of domain to connect to
# 0.007635084999999998 - group-ib.com
# 0.008298706999999995 - kaspersky.com
# 0.0041737319999999994 - mai.ru
# 0.007643109000000002 - www.gosuslugi.ru
# 0.006321244999999996 - www.microsoft.com
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket
s.settimeout(5) # set timeout
sslSocket = context.wrap_socket(s, server_hostname = dn) # wrap socket into TLS context

try:
    begin = time.process_time() # start timer
    sslSocket.connect((dn, 443)) # TLS socket connection
    perf = time.process_time() - begin # end timer

    print ("Success! Performance time for TLS connection is: ", perf) #convert from sec. to ms by multiplying with 1000


except (ssl.SSLError, ssl.SSLEOFError, ssl.CertificateError,ssl.SSLSyscallError, ssl.SSLWantWriteError, ssl.SSLWantReadError,ssl.SSLZeroReturnError) as e1:
    sslSocket.close() # close the socket
except Exception as e2:
    sslSocket.close() # close the socket