import sqlite3
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
                    first_name VARCHAR,
                    last_name VARCHAR,
                    date_of_birth DATE,
                    phone_number REAL,
                    id_number REAL,
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
        res = input("Temperature: " + str(statistics.mode(data[0])) + "\n1. Continue \t 2. Record Again\n")
        if res == "2":
            get_temperature()

        return statistics.mode(data[0])
    
    elif reading == 'heart_rate':
        res = input("Heart Rate: " + str(statistics.mode(data[0])) + "\n1. Continue \t 2. Record Again\n")
        if res == "2":
            get_heartrate()

        return statistics.mode(data[0])
    
    else:
        return


def get_temperature():
    serial_getter("2")
    temperature = getmode("temperature")
    return temperature


def get_heartrate():

    serial_getter("1")
    heart_rate = getmode("heart_rate")
    return heart_rate
    

def register():
    phone_number = input("Phone Number: ")
    national_id = input("National ID: ")
    if national_id=="" and phone_number=="":
        print("Provide Phone Number or National ID")
        register()
    else:
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        date_of_birth = input("Date of Birth: ")
        location = input("Location: ")
        pregnancy_type = input("Pregnancy Type: ")
        expected_delivery_date = input("EDD: ")
        pregnancy_count = input("Pregnancy Count: ")
        height = input("Height: ")
        weight = input("Weight: ")
        temperature = get_temperature()
        heart_rate = get_heartrate()

        data = (str(national_id), str(phone_number), str(first_name), str(last_name), str(date_of_birth), str(location), str(pregnancy_type), str(expected_delivery_date), str(pregnancy_count), float(height), float(weight), float(temperature), float(heart_rate))
        cursor.execute(
            "INSERT INTO fetal_hrm_data(id_number,phone_number,first_name,last_name, date_of_birth, location,pregnancy_type,expected_delivery_date,pregnancy_count,height,weight,temperature,heart_rate)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
        connection.commit()
        print("Record Saved Successfully\n")
        main_menu()


def new_member():
    action = input("1: Register \n2: Record Vitals\n")
    if action == "1":
        register()
    elif action == "2":
        get_temperature()
        get_heartrate()
        main_menu()
    else:
        print("Invalid Optio1n\n")
        new_member()

def registered_member():
    identifier = input("\nUse Identifier \n1: Phone Number \n2: National ID\n")
    if identifier == "1":
        phone_number = input("2Enter Phone Number: ")
        if phone_number == "":
            print("Phone Number is Required")
            registered_member()
        else:
            height = input("Height: ")
            weight = input("Weight: ")
            temperature = get_temperature()
            heart_rate = get_heartrate()

            data = (str(phone_number), float(weight), float(height), float(temperature), float(heart_rate))
            cursor.execute("INSERT INTO fetal_hrm_data(phone_number,weight,height,temperature,heart_rate)VALUES(?,?,?,?,?)", data)
            connection.commit()
            print("Data Saved Successfully!\n")
            main_menu()
    elif identifier == "2":
        national_id = input("Enter National ID: ")
        if national_id == "":
            print("National ID is Required")
            registered_member()
        else:
            height = input("Height: ")
            weight = input("Weight: ")
            temperature = get_temperature()
            heart_rate = get_heartrate()

            data = (str(national_id), float(weight), float(height), float(temperature), float(heart_rate))
            cursor.execute("INSERT INTO fetal_hrm_data(id_number,weight,height,temperature,heart_rate)VALUES(?,?,?,?,?)", data)
            connection.commit()
            print("Data Saved Successfully!\n")
            main_menu()
    else:
        print("Invalid Option\n")
        registered_member()


def main_menu():
    check_existence = input("Registered Member? \n1: Yes \n2: No\n")
    if check_existence == '1':
        registered_member()
    elif check_existence == '2':
        new_member()
    else:
        print("Invalid Option\n")
        main_menu()

print("Fetal Heart Rate Monitor...\n")
main_menu()