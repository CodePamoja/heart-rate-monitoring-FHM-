import sqlite3
import uuid
import serial
import statistics
import pandas as pd
import socket

try:
    connection = sqlite3.connect("Fetal.db")
    cursor = connection.cursor()

except sqlite3.Error as error:
    print("Database Error", error)

sql_create_table = """CREATE TABLE IF NOT EXISTS fetal_hrm_data  (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    uuid VARCHAR,
                    first_name VARCHAR,
                    last_name VARCHAR,
                    date_of_birth DATE,
                    phone_number VARCHAR,
                    id_number VARCHAR,
                    location VARCHAR,
                    pregnancy_type VARCHAR,
                    expected_delivery_date DATE,
                    pregnancy_count VARCHAR,
                    health_centre VARCHAR,
                    height REAL,
                    weight REAL,
                    temperature REAL,
                    heart_rate REAL,
                    fetal_heart_rate REAL,
                    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                    server_sync INTEGER DEFAULT 0
                    );"""
cursor.execute(sql_create_table)


def serial_getter(x):
    ser = serial.Serial("COM9 (Arduino/Genuino Uno)")
    ser.baudrate = '115200'

    if x == "1":
        ser.write(1)
        open("data.txt", "wb")
        count = 100
        while count > 0:
            f = open("data.txt", "ab")
            f.write(ser.readline())
            print("." * count)
            count -= 1

        print("Heart Rate Recorded!\n")
        f.close()
        ser.close()

    elif x == "2":
        ser.write(2)
        open("data.txt", "wb")
        count = 100
        while count > 0:
            f = open("data.txt", "ab")
            f.write(ser.readline())
            print("." * count)
            count -= 1

        print("Temperature Recorded!\n")
        f.close()
        ser.close()


def getmode(reading):

    data = pd.read_table(r"data.txt", header=None, usecols=[0])
    
    if reading == 'temperature':
        res = input("Temperature: " + str(statistics.mode(data[0])) + "\n1. Continue \t 2. Record Again \n00: Exit\n")
        if res == "2":
            get_temperature()
        elif res == "00":
            main_menu()
        else:
            return statistics.mode(data[0])
    
    elif reading == 'heart_rate':
        res = input("Heart Rate: " + str(statistics.mode(data[0])) + "\n1. Continue \t 2. Record Again \n00: Exit\n")
        if res == "2":
            get_heartrate()
        elif res == "00":
            main_menu()
        else:
            return statistics.mode(data[0])
    
    else:
        return


def record_vitals():
    global height
    height = input("Height: ") 
    global weight
    weight = input("Weight: ") 
    sensor_vitals()
    
    
def sensor_vitals():
    record = input("\nRecord \n1: Temperature \n2: Heart Rate \n3: Continue\n")
    if record == '1':
        global temperature
        temperature = get_temperature()
        sensor_vitals()
    elif record == '2':
        global heart_rate
        heart_rate = get_heartrate()
        sensor_vitals()
    elif record == '3':
        return
    else:
        print("Invalid Option\n")
        sensor_vitals()

def get_temperature():
    #print('Recording Temperature')
    #serial_getter("2")
    #temperature = getmode("tfloat() argument must be a string or a number, not 'NoneType'emperature")
    temperature = input("Temperature: ")
    
    return temperature


def get_heartrate():
    #print('Place finger of Sensor to Record Heart Rate')
    #serial_getter("1")
    #heart_rate = getmode("heart_rate")
    heart_rate = input("Heart Rate: ")
    return heart_rate
    

def register():
    global phone_number
    phone_number = input("Phone Number: ")
    global national_id
    national_id = input("National ID: ")
    if national_id=="" and phone_number=="":
        print("Provide Phone Number or National ID")
        register()
    else:
        global first_name
        first_name = input("First Name: ")
        global last_name
        last_name = input("Last Name: ")
        global date_of_birth
        date_of_birth = input("Date of Birth: ")
        global location
        location = input("Location: ")
        global pregnancy_type
        pregnancy_type = input("Pregnancy Type: ")
        global expected_delivery_date
        expected_delivery_date = input("EDD: ")
        global pregnancy_count
        pregnancy_count = input("Pregnancy Count: ")
        save_new()
        print("\nRecord Vitals. . .")
        registered_member()
        main_menu()


def new_member():
    action = input("\n1: Register \n2: Record Vitals \n0: Back \t00: Exit\n")
    if action == "1":
        register()
    elif action == "2":
        get_temperature()
        get_heartrate()
        main_menu()
    elif action == '0':
        main_menu()
    elif action == '00':
        exit()
    else:
        print("Invalid Option\n")
        new_member()

def registered_member():
    identifier = input("\nUse Identifier to Record \n1: Phone Number \n2: National ID \n0: Menu \t00: Exit\n")
    if identifier == "1":
        phone_number = input("Enter Phone Number: ")
        national_id = ""
        if phone_number == "":
            print("Phone Number is Required")
            registered_member()
        else:
            record_vitals()
            save_existing('',phone_number)
            main_menu()
    elif identifier == "2":
        national_id = input("Enter National ID: ")
        phone_number = ""
        if national_id == "":
            print("National ID is Required")
            registered_member()
        else:
            record_vitals()
            save_existing(national_id,'')
            main_menu()
    elif identifier == '0':
        main_menu()
    elif identifier == '00':
        exit()
    else:
        print("Invalid Option\n")
        registered_member()

def save_existing(id_no,phone):
    if id_no == '':
        data = (str(uuid.uuid4().hex), str(phone), float(weight), float(height), float(temperature), float(heart_rate))
        cursor.execute("INSERT INTO fetal_hrm_data(uuid,phone_number,weight,height,temperature,heart_rate)VALUES(?,?,?,?,?,?)", data)
        connection.commit()
        print("Data Saved Successfully!\n")
        return
    else:
        data = (str(uuid.uuid4().hex), str(id_no), float(weight), float(height), float(temperature), float(heart_rate))
        cursor.execute("INSERT INTO fetal_hrm_data(uuid,id_number,weight,height,temperature,heart_rate)VALUES(?,?,?,?,?,?)", data)
        connection.commit()
        print("Data Saved Successfully!\n")
        return


def save_new():
    data = (str(uuid.uuid4().hex), str(national_id), str(phone_number), str(first_name), str(last_name), str(date_of_birth), str(location), str(pregnancy_type), str(expected_delivery_date), str(pregnancy_count))
    cursor.execute(
        "INSERT INTO fetal_hrm_data(uuid,id_number,phone_number,first_name,last_name, date_of_birth, location,pregnancy_type,expected_delivery_date,pregnancy_count)VALUES(?,?,?,?,?,?,?,?,?,?)", data)
    connection.commit()
    print("Record Saved Successfully\n")
    

def sub_menu():
    print("\nFetal Heart Rate Monitor...\n")
    option = input("Select Option... \n1: Record Patient Data \n2: Send Data to Server \n0: Exit\n")
    if option == '1':
        main_menu()
    elif option == '2':
        print('Sending data to server...')
    elif option == '0':
        exit()
    else:
        print("Invalid Option\n")
        sub_menu()
    
    
    
def main_menu():
    check_existence = input("\nRegistered Member? \n1: Yes \n2: No \n0: Main Menu \t00: Exit\n")
    if check_existence == '1':
        registered_member()
    elif check_existence == '2':
        new_member()
    elif check_existence == '0':
        sub_menu()
    elif check_existence == '00':
        exit()
    else:
        print("Invalid Option\n")
        main_menu()

print("Fetal Heart Rate Monitor...")
main_menu()