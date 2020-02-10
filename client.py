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


def delete_data():
    from_server = client.recv(4096)
    received = from_server.decode("utf-8")
    cur.execute("SELECT id FROM fetal_hrm_data ")
    array = cur.fetchone()
    str1 = ''.join(str(e) for e in array)  # list to string from db
    char2 = str1[0]
    for n in received:
        if n == char2:
            x = cur.execute("DELETE FROM fetal_hrm_data WHERE id=?", (char2,))
            while x:
                print('records deleted')
                break


def send_message(dat):
    dataa = json.dumps(dat)
    client.send(bytes(dataa, "utf-8"))


data = []
for i in range(len(myresult1)):
    message = json.dumps \
        ({"id": myresult1[i][0], "uuid": myresult1[i][1], "first_name": myresult1[i][2], "last_name": myresult1[i][3],
          "date_of_birth": myresult1[i][4], "phone_number": myresult1[i][5],
          "id_number": myresult1[i][6],
          "location": myresult1[i][7], "pregnancy_type": myresult1[i][8],
          "expected_delivery_date": myresult1[i][9],
          "pregnancy_count": myresult1[i][10], "health_center": myresult1[i][11],
          "height": myresult1[i][12],
          "weight": myresult1[i][13], "temparature": myresult1[i][14],
          "heart_rate": myresult1[i][15],
          "fetal_heart_rate": myresult1[i][16], "date_created": myresult1[i][17]})
    messaged = json.loads(message)
    data.append(messaged)

send_message(data)
delete_data()
