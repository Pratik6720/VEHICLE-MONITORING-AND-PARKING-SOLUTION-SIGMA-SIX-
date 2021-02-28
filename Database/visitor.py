import psycopg2
from prettytable import PrettyTable

x = PrettyTable()

try:
    connection = psycopg2.connect(user="",
                                  password="",
                                  host="",
                                  port="",
                                  database="")  # Database connection
    # print("connected")

    # create a cursor object
    cursor = connection.cursor()
    resident_tb = cursor.execute("SELECT * from visitor")

    rows = cursor.fetchall()
    for row in rows:
        list = []
        x.field_names = ["SR NO","VISITOR NAME","NUMBER PLATE","MOBILE NUMBER","ENTRY TIME"]
        for i in range(0,5):
            list.append(row[i])
            # print(row[i],end=" | ")
        x.add_row(list)

    print(x)
except IOError:
    print("Fail to connect")

finally:
    connection.close()
