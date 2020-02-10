import psycopg2
from time import ctime

res_name = None


def slot_allot(plate_value, slot_value):
    # print('value from exp file is :', plate_value)
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="mydbinstance.cjfxaiq2xh1x.us-east-2.rds-preview.amazonaws.com",
                                      port="5432",
                                      database="sih2020")
        # print("Allot also connected")
        # print("--------------------")
        # select * from resident where slot_value = {}
        # create a cursor object
        print("---------------------------------------------------------------")
        cursor = connection.cursor()
        cursor.execute("SELECT * from resident")
        rows = cursor.fetchall()

        flag = 0
        for row in rows:
            if slot_value == row[4]:
                rt1 = cursor.execute("SELECT reg_name , no_plate , mobile_number , alloted_slot from resident")
                rt = cursor.fetchone()

                res_name = row[1]
                res_mo = row[3]
                print("Slot is alloted to : ", res_name)
                if plate_value == row[2]:
                    flag = 1
                    print('ok ok')
                    print("allotted number plate is :", row[2])
                    print("---------------------------------------------------------------")

                # print("Number Plate =", row[1])
                # rt2 = cursor.execute("'".format(plate_value, ctime(), row[0]))
                # connection.commit()
                break

        if flag != 1:
            p1 = cursor.execute("SELECT * from resident where no_plate = '{}'".format(plate_value))
            pt = cursor.fetchone()
            current_name = pt[1]
            current_mobile_number = pt[3]
            print("This person parked at your place:", current_name)
            print("The wrong person's mobile number is:", current_mobile_number)
            p2 = cursor.execute(
                "UPDATE  resident set current_name = '{0}', current_mo = '{1}'  where reg_name = '{2}'".format(
                    current_name, current_mobile_number, res_name))
            connection.commit()


    except IOError:
        print("Fail to connect")

    finally:
        connection.close()

slot_allot('GJ18BG5803',5)
