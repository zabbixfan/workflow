import socket
def singleCheck(ip):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip,22))
        # print "{}:{},{}".format(ip,22,'success')
        res = True
    except Exception,e:
        # print "{}:{},{}".format(ip, 22, e)
        res = False
        # print str(e)

    finally:
        s.close()
    return res