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

        file = open("rawData.json", "wb")
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

""" Connect to the PostgreSQL database server """
con = None

print('Connecting to the PostgreSQL database...')
try:
    con = psycopg2.connect(host="localhost",database="fetal_hrm", user="pi", password="123")
    cursor = con.cursor()

    with open('rawData.json', 'r') as client_data:
        client_dict = json.load(client_data)

    for data_object in client_dict:
        sql = """INSERT INTO monitor_readings(uuid,height,weight,temperature,heart_rate,client_created) VALUES(%s,%s,%s,%s,%s,%s);"""
        data = (data_object['uuid'], data_object['height'], data_object['weight'], data_object['temperature'], data_object['heart_rate'], data_object['date_created'])
        cursor.execute(sql,data)
        con.commit()
    print('Data saved succesfuly')

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
        if con is not None:
            con.close()
            print('Database connection closed.')
