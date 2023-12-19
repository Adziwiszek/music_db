import socket
import requests

res = requests.get("http://localhost:5000/osoba/123")
print(res.json())
res = requests.put("http://localhost:5000/osoba")
print(res.json())

# port = 8081
# host = "localhost"
# s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# message = 'Hello Python!!!'
# mes_bytes = message.encode('utf-8')
# s.sendto(mes_bytes, (host, port))