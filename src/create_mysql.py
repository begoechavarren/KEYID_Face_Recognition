import mysql.connector
from dotenv import load_dotenv
import os


def create_mySQLTable():
    load_dotenv()
    sql_password = os.getenv("sql_password")

    # Create mySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=sql_password
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS employees")

    # Create mySQL table
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=sql_password,
        database="employees"
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS employee_signatures (name VARCHAR(255), action VARCHAR(255), time DATETIME)")


create_mySQLTable()
