import socket,json
s = socket.socket()
host = '192.168.255.170'
port = 6212
data = {
    "data":{"services":[
        {"projectName": "CustomerCenter","type":"Java:War","ip":["192.168.100.34"]},
        {"projectName": "order-service", "type": "Java:Jar", "ip": ["192.168.100.34"]}
    ]},
    "id": "33213",
    "type": "restartProject"
}
try:
    s.connect((host,port))
    s.sendall(json.dumps(data))
    recv = s.recv(1024)
    print recv
except Exception as e:
    print e
finally:
    s.close()