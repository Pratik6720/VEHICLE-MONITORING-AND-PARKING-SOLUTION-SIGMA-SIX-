from datetime import datetime

import psycopg2

def checkValue(plate_value):
    try:
        connection = psycopg2.connect(user="",
                                      password="",
                                      host="",
                                      port="",
                                      database="")     #Database connection
        # print("connected")

        # create a cursor object
        cursor = connection.cursor()
        cursor.execute("SELECT sr_no , reg_name , no_plate , mobile_number from resident")
        rows = cursor.fetchall()

        flag = 0
        for row in rows:
            if plate_value == row[2]:
                flag = 1

                # rt = cursor.execute("SELECT no_plate from residence")
                rt1 = cursor.execute("SELECT sr_no , reg_name , no_plate , mobile_number from resident")
                print("----------------------------------------")
                print("Found This Number Plate Data In Database")
                print("This is a Residents car")
                print("----------------------------------------")

                # rt = cursor.fetchall()

                rt1 = cursor.fetchall()


                # print("REGISTER NAME =", row[1])
                # print("VEHICLE NUMBER PLATE =", row[2])
                # print("MOBILE NUMBER =", row[3], "\n")

        if flag != 1:
            print("This Number Plate Isn't Found In Database")
            print("This is a visitors car")
            print("Inserting Visitor Number Plate In Database ")
            coun = 1
            rt2 = cursor.fetchall()

            # cursor.execute("SELECT sr_no , name , no_plate , mobile_number from rto_dummy")
            cursor.execute("SELECT sr_no , vi_no_plate , time from visitor")
            row1 = cursor.fetchall()
            # row1 = cursor.fetchall()
            # cursor.execute("insert into  visitor(vi_no_plate,time) values('{}',%s)  ".format(plate_value))
            # cursor.execute("SELECT name, mobile_number from rto_dummy where no_plate = '{}'".format(plate_value))
            # rt2 = cursor.fetchone()
            # #cursor.execute("SELECT mobile_number from rto_dummy where no_plate = '{}'".format(plate_value))
            # #rt3 = cursor.fetchone()

            cursor.execute(
                "INSERT INTO visitor ( vi_no_plate, time) VALUES ( '{0}' ,"
                "'{1}')".
                format( plate_value, datetime.now()))

            # for row in row1,rt2:
            #     if rt2[1] == row1[2]:
            #         cursor.execute("INSERT INTO visitor (sr_no,vis_name, vi_no_plate,mobile_number, time) VALUES (sr_no, '{0}' ,"
            #                "'{1}', '{2}' , ' {3} ')".
            #                format(rt2[0],plate_value,rt2[1],datetime.now()))

            # postgres_insert_query = """INSERT INTO visitor (vis_name, vi_no_plate,mobile_number, time) VALUES (%s,%s,%s,%s)"""
            # insert_data = (rt2[0], plate_value,rt2[1], datetime.now())
            # # cursor.execute("INSERT INTO visitor (vis_name,vi_no_plate,mobile_number,time) values (%s,%s,%s,%s)")
            # rt3 = cursor.execute(postgres_insert_query, insert_data)

            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into visitor table")
            print("----------------------------------------")

    except IOError:
        print("Fail to connect")

    finally:
        connection.close()


# checkValue(plate_value)
