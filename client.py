import json
import sqlite3 as sqlite
import socket

def main():
	global client 
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(('192.168.0.75', 12345))
	global con 
	con = sqlite.connect('Fetal.db')

	with con:
	    global cur 
	    cur = con.cursor()
	    cur.execute("SELECT * FROM fetal_hrm_data")
	    myresult1 = cur.fetchall()

	data = []
	for i in range(len(myresult1)):
	    message = json.dumps({"id": myresult1[i][0], "uuid": myresult1[i][1], "first_name": myresult1[i][2], "last_name": myresult1[i][3],
	          "date_of_birth": myresult1[i][4], "phone_number": myresult1[i][5],
	          "id_number": myresult1[i][6],
	          "location": myresult1[i][7], "pregnancy_type": myresult1[i][8],
	          "expected_delivery_date": myresult1[i][9],
	          "pregnancy_count": myresult1[i][10], "health_center": myresult1[i][11],
	          "height": myresult1[i][12],
	          "weight": myresult1[i][13], "temperature": myresult1[i][14],
	          "heart_rate": myresult1[i][15],
	          "fetal_heart_rate": myresult1[i][16], "date_created": myresult1[i][17]})
	    messaged = json.loads(message)
	    data.append(messaged)

	dataa = json.dumps(data)
	client.send(bytes(dataa, "utf-8"))
	print("Data sent to Server...")

	delete_data()


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
	    	response = json.loads(received)
	    	print("Response received from server...")
	    	for obj in response:
	    		cur.execute("UPDATE fetal_hrm_data SET server_sync = 1 WHERE uuid =? ",(obj,))
	    	con.commit()
	    	print("Local Database Updated Successfully...")
	except con.Error as error:
		print("Error updating local Database",error)
	finally:
		if (con):
			con.close()
			print("Database Connection Closed.")


if __name__ == "__main__":
    main()