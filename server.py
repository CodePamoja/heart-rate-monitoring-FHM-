import socket
import json
import psycopg2

def save_data():
    """ Connect to the PostgreSQL database server """
    con = None
    saved = []

    print('Connecting to the PostgreSQL database...')
    try:
        con = psycopg2.connect(host="localhost",database="fetal_hrm", user="pi", password="123")
        con.autocommit = True
        cursor = con.cursor()

        with open('rawData.json', 'r') as client_data:
            client_dict = json.load(client_data)

        for data_object in client_dict:
            if data_object['first_name'] == None:
                if data_object['phone_number'] == None:
                    idno_sql = """INSERT INTO monitor_readings(uuid,id_number,height,weight,temperature,heart_rate,fetal_heart_rate,client_created) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""
                    idno_data = (data_object['uuid'], data_object['id_number'], data_object['height'], data_object['weight'], data_object['temperature'], data_object['heart_rate'], data_object['fetal_heart_rate'], data_object['date_created'])
                    try:
                        cursor.execute(idno_sql,idno_data)
                        saved.append(data_object['uuid'])
                    except (Exception, psycopg2.DatabaseError) as error:
                        print(error)
                    
                else:
                    phone_sql = """INSERT INTO monitor_readings(uuid,phone_number,height,weight,temperature,heart_rate,fetal_heart_rate,client_created) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""
                    phone_data = (data_object['uuid'], data_object['phone_number'], data_object['height'], data_object['weight'], data_object['temperature'], data_object['heart_rate'], data_object['fetal_heart_rate'], data_object['date_created'])
                    try:
                        cursor.execute(phone_sql,phone_data)
                        saved.append(data_object['uuid'])
                    except (Exception, psycopg2.DatabaseError) as error:
                        print(error)
            else:
                maternal_sql = """INSERT INTO maternal_information(uuid,first_name,last_name,date_of_birth,phone_number,id_number,client_created) VALUES(%s,%s,%s,%s,%s,%s,%s);"""
                maternal_data = (data_object['uuid'], data_object['first_name'], data_object['last_name'], data_object['date_of_birth'], data_object['phone_number'], data_object['id_number'],data_object['date_created'])
                
                pregnancy_sql = """INSERT INTO pregnancy_information(maternal_uuid,location,pregnancy_type,expected_delivery_date,pregnancy_count) VALUES(%s,%s,%s,%s,%s);"""
                pregnancy_data = (data_object['uuid'], data_object['location'], data_object['pregnancy_type'], data_object['expected_delivery_date'], data_object['pregnancy_count'])
                try:
                    cursor.execute(maternal_sql,maternal_data)
                    cursor.execute(pregnancy_sql,pregnancy_data)
                    saved.append(data_object['uuid'])
                except (Exception, psycopg2.DatabaseError) as error:
                        print(error)

        print('The following was Saved Successfully')
        print(saved, sep='\n')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
            if con is not None:
                con.close()
                print('Database connection closed.')

    return saved


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('socket successfully created')
serv.bind(('192.168.0.75', 12345))
print('socket bound')
serv.listen(5)
while True:
    conn, addr = serv.accept()
    print('Got connection from', addr)
    data = conn.recv(4096)
    if not data:
        break

    file = open("rawData.json", "wb")
    file.write(data)
    file.close()
        
    arry = save_data()

    conn.send(bytes(json.dumps(arry), "utf-8"))
    conn.close()
    print('client disconnected')