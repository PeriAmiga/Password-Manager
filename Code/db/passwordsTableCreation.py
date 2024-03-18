import mysql.connector
from db import dbConnection

def passwordsTblCreation(connection):

    # Create a new cursor
    cursor = connection.cursor()

    # Check if the 'passwords' table already exists
    checkTableQuery = "SHOW TABLES LIKE 'passwords'"
    cursor.execute(checkTableQuery)
    existingTables = cursor.fetchall()

    if not existingTables:
        # If 'passwords' table doesn't exist, create it
        createTableQuery = """
        CREATE TABLE `passwords` (
            `id` INT(20) unsigned NOT NULL AUTO_INCREMENT,
            `user` VARCHAR(128) NOT NULL,
            `name` VARCHAR(255) NOT NULL,
            `url` VARCHAR(255),
            `username` VARCHAR(128) NOT NULL,
            `password` VARCHAR(128) NOT NULL,
            KEY `user_index` (`user`) USING BTREE,
            PRIMARY KEY (`id`)
        )
        """

        try:
            # Execute the SQL query to create the table
            cursor.execute(createTableQuery)
            print("Table 'passwords' created successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    else:
        print("Table 'passwords' already exists in the database.")

    cursor.close()