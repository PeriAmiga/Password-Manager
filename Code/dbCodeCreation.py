from db import schemaCreation
from db import dbConnection
from db import passwordsTableCreation
from db import usersTableCreation


#Create schema and db if doesn't exist
schemaCreation.schemaCreate()
connection = dbConnection.dbConnect()
usersTableCreation.usersTblCreation(connection)
passwordsTableCreation.passwordsTblCreation(connection)
connection.close()