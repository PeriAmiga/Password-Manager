import mysql.connector
from db import dbConnection

# Connection to the database in MySQL
def schemaCreate():
    conn = dbConnection.schemaCreate()
    cursor = conn.cursor()

    try:

        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS PasswordManager;")

        # Commit the changes to the database
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and the connection
        cursor.close()
        conn.close()