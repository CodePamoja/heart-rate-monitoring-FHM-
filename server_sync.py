import psycopg2
import json

""" Connect to the PostgreSQL database server """
con = None

print('Connecting to the PostgreSQL database...')
try:
    con = psycopg2.connect(host="localhost",database="fetal_hrm", user="postgres", password="123")
    cursor = con.cursor()

    with open('rawData.json', 'r') as client_data:
        client_dict = json.load(client_data)

    for data_object in client_dict:
        if data_object['first_name'] == None:
            if data_object['phone_number'] == None:
                idno_sql = """INSERT INTO monitor_readings(uuid,id_number,height,weight,temperature,heart_rate,fetal_heart_rate,client_created) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""
                idno_data = (data_object['uuid'], data_object['id_number'], data_object['height'], data_object['weight'], data_object['temperature'], data_object['heart_rate'], data_object['fetal_heart_rate'], data_object['date_created'])
                cursor.execute(idno_sql,idno_data)
                con.commit()
            else:
                phone_sql = """INSERT INTO monitor_readings(uuid,phone_number,height,weight,temperature,heart_rate,fetal_heart_rate,client_created) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""
                phone_data = (data_object['uuid'], data_object['phone_number'], data_object['height'], data_object['weight'], data_object['temperature'], data_object['heart_rate'], data_object['fetal_heart_rate'], data_object['date_created'])
                cursor.execute(phone_sql,phone_data)
                con.commit()
        else:
            maternal_sql = """INSERT INTO maternal_information(uuid,first_name,last_name,date_of_birth,phone_number,id_number,client_created) VALUES(%s,%s,%s,%s,%s,%s,%s);"""
            maternal_data = (data_object['uuid'], data_object['first_name'], data_object['last_name'], data_object['date_of_birth'], data_object['phone_number'], data_object['id_number'],data_object['date_created'])
            
            pregnancy_sql = """INSERT INTO pregnancy_information(maternal_uuid,location,pregnancy_type,expected_delivery_date,pregnancy_count) VALUES(%s,%s,%s,%s,%s);"""
            pregnancy_data = (data_object['uuid'], data_object['location'], data_object['pregnancy_type'], data_object['expected_delivery_date'], data_object['pregnancy_count'])
            
            cursor.execute(maternal_sql,maternal_data)
            cursor.execute(pregnancy_sql,pregnancy_data)
            con.commit()

    print('Data saved succesfuly')

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
        if con is not None:
            con.close()
            print('Database connection closed.')
