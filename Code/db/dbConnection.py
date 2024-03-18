import mysql.connector
from db import configuration


#Connection to the database in MySQL
def schemaCreate():
    conn = mysql.connector.connect(
        host= configuration.dbHost,
        user= configuration.dbUser,
        password= configuration.dbPassword,
    )
    return conn


#Connection to the database in MySQL
def dbConnect():
    conn = mysql.connector.connect(
        host= configuration.dbHost,
        user= configuration.dbUser,
        password= configuration.dbPassword,
        database= 'PasswordManager',
    )
    return conn