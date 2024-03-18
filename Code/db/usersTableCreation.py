import mysql.connector
from db import dbConnection

def usersTblCreation(connection):

    # Create a new cursor
    cursor = connection.cursor()

    #Check if the 'users' table already exists
    checkTableQuery = "SHOW TABLES LIKE 'users'"
    cursor.execute(checkTableQuery)
    existingTables = cursor.fetchall()

    if not existingTables:
        #If 'users' table doesn't exist, create it
        createTableQuery = """
        CREATE TABLE `users` (
            `id` INT(20) unsigned NOT NULL AUTO_INCREMENT,
            `email` VARCHAR(320) NOT NULL,
            `username` VARCHAR(128) COLLATE utf8_bin NOT NULL,
            `password` VARCHAR(128) COLLATE utf8_bin NOT NULL,
            UNIQUE KEY `username_index` (`username`) USING BTREE,
            UNIQUE KEY `email_index` (`email`) USING BTREE,
            PRIMARY KEY (`id`)
        )
        """

        try:
            # Execute the SQL query to create the table
            cursor.execute(createTableQuery)
            print("Table 'users' created successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    else:
        print("Table 'users' already exists in the database.")

    cursor.close()