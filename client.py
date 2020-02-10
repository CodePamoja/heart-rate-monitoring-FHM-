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
	try:
	    from_server = client.recv(4096)
	    received = from_server.decode("utf-8")
	    cur.execute("SELECT id FROM fetal_hrm_data ")
	    array = cur.fetchone()
	    if array == None:
	    	print('no data in database')
	    	con.close()
	    	print('database connection is closed')
	    else:
		    str1 = ''.join(str(e) for e in array)  # list to string from db
		    char2 = str1[0]
		    for n in received:
		        if n == char2:
		            x = cur.execute("""DELETE from fetal_hrm_data where id =? """ , (char2,))
		            con.commit()
		            print("Record deleted successfully ")
		            cur.close()
	except con.Error as error:
		print("Failed to delete record from database ",error)
	finally:
		if (con):
			con.close()
			print("the database connection is closed")


def send_message(dat):
    dataa = json.dumps(dat)
    client.send(bytes(dataa, "utf-8"))


data = []
for i in range(len(myresult1)):
    message = json.dumps \
        ({"id": myresult1[i][0], "first_name": myresult1[i][1], "last_name": myresult1[i][2],
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
delete_data()
