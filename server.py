import socket
import json
import psycopg2

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('socket succesfuly created')
serv.bind(('localhost', 12345))
print('socket bound')
serv.listen(5)
while True:
    conn, addr = serv.accept()
    print('Got connection from', addr)
    from_client = ''
    while True:
        data = conn.recv(4096)
        if not data:
            break

        file = open("rawData", "wb")
        file.write(data)
        file.close()

        x = data.decode("utf-8")
        arry = []
        for y in json.loads(x):
            arry.append(y["id"])
            print(y["id"])

        conn.send(bytes(json.dumps(arry), "utf-8"))
        conn.close()
        print('client disconnected')
