import psycopg2
import videoallot as vs
import time

def slot_remove(plate_value):
    # print('value from exp file is :', plate_value)
    try:
        connection = psycopg2.connect(user="",
                                      password="",
                                      host="",
                                      port="",
                                      database="")
        # if the number plate is found in parking record database it means that the particular car is already parked and is exiting
        # if the number plate is not found in parking record database means it is entering for the first time
        # so it allots the slot to that car
        print("Checking if there is a parking of this plate value")

        # create a cursor object
        cursor = connection.cursor()
        cursor.execute("SELECT slot_no , no_plate from commercial_parking")
        rows = cursor.fetchall()

        flag = 0
        for row in rows:
            # print("plate inside function",plate_value)

            if plate_value == row[1]:
                print("---------------------------------------------------------------")
                flag = 1

                rt1 = cursor.execute("SELECT slot_no , no_plate , exit_time from commercial_parking")
                rt = cursor.fetchall()
                print("Plate found in our record so removing it from our record")
                print("Vehicle removed from Slot number is : ", row[0])
                print("Removed vehicle number plate is :", row[1])
                print("Exit time :",time.ctime())
                print("---------------------------------------------------------------")
                connection.commit()
                rt2 = cursor.execute("UPDATE commercial_parking set no_plate = NULL "
                                     "  WHERE no_plate = '{}'".format(plate_value))

                connection.commit()
                break

                # vs.slot_allot(plate_value)
        if flag != 1:
            vs.slot_allot(plate_value)




    except IOError:
        print("Fail to connect")

    finally:
        connection.close()
    return True

# For static values you can check by directly calling the function and passing the number plate in it
#slot_remove('GJ01RM9874')
#vs.slot_allot('GJ18AB5645')
