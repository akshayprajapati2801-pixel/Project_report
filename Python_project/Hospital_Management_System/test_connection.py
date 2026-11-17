from database.connection import Database


try:

    database = Database()

    connection = database.get_connection()

    print("================================")
    print("MySQL CONNECTION SUCCESSFUL")
    print("================================")

    connection.close()

except Exception as error:

    print("================================")
    print("MYSQL CONNECTION FAILED")
    print("================================")
    print(error)