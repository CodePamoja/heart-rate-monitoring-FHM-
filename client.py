import json
import sqlite3 as sqlite
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))
con = sqlite.connect('Fetal.db')

with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM fetal_hrm_data")
    myresult1 = cur.fetchall()
    # print(myresult1[1][2:5])


def delete_table():
    from_server = client.recv(4096)
    print(from_server.decode("utf-8"))



def send_message(dat):
    dataa = json.dumps(dat)
    client.send(bytes(dataa, "utf-8"))


data = []
for i in range(len(myresult1)):
    message = json.dumps({"id": myresult1[i][0], "first_name": myresult1[i][1], "last_name": myresult1[i][2],
                          "date_of_birth": myresult1[i][3], "phone_number": myresult1[i][4],
                          "id_number": myresult1[i][5],
                          "location": myresult1[i][6], "pregnancy_type": myresult1[i][7],
                          "expected_delivery_date": myresult1[i][8],
                          "pregnancy_count": myresult1[i][9], "health_center": myresult1[i][10],
                          "height": myresult1[i][11],
                          "weight": myresult1[i][12], "temparature": myresult1[i][13],
                          "heart_rate": myresult1[i][14],
                          "fetal_heart_rate": myresult1[i][15], "date_created": myresult1[i][16]})
    messaged = json.loads(message)
    data.append(messaged)

send_message(data)
delete_table()
