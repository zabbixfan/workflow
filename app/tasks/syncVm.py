#!coding:utf-8
import socket,json,logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s",
    filename="app.log",
    filemode="a+"
)
def sync_xenVm():
    host = '192.168.255.170'
    port = 6212
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    data = json.dumps({
        "type": "scanInternalDataCenter"
    })
    socket.setdefaulttimeout(1)
    try:
        s.connect((host, port))
        s.sendall(data)
        print s.recv(1024)
    except Exception as e:
        logging.error('sync_xenVm failed,agent {}:{},{}'.format(host,port,str(e)))
    finally:
        s.close()
    return None

sync_xenVm()