import psycopg2

""" Connect to the PostgreSQL database server """
con = None

print('Connecting to the PostgreSQL database...')
try:
    con = psycopg2.connect(host="localhost",database="fetal_hrm", user="postgres", password="123")
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
