import psycopg2
from time import ctime
def slot_allot(plate_value):
    # print('value from exp file is :', plate_value)
    try:
        connection = psycopg2.connect(user="",
                                      password="",
                                      host="",
                                      port="",
                                      database="")

        print("This plate is not found in our record so alloting slot to this:")
        print("---------------------------------------------------------------")

        # create a cursor object
        cursor = connection.cursor()
        cursor.execute("SELECT slot_no  , no_plate from commercial_parking")
        rows = cursor.fetchall()

        flag = 0
        for row in rows:
            if row[1] == None:
                flag = 1
                rt1 = cursor.execute("SELECT slot_no , no_plate , entry_time from commercial_parking")
                rt = cursor.fetchall()
                print("Please Park at Slot no. =", row[0])
                print("Parked vehicle number plate is :", plate_value)
                print("Entry time is :" , ctime())
                print("---------------------------------------------------------------")

                # print("Number Plate =", row[1])
                rt2 = cursor.execute(
                    "UPDATE commercial_parking set no_plate = '{0}',entry_time = '{1}' WHERE slot_no = {2}".format(plate_value,ctime(), row[0]))
                connection.commit()
                break

        if flag != 1:
            print("No Empty Space Found")
            print("Parking is now full sorry for inconvinience")

    except IOError:
        print("Fail to connect")

    finally:
        connection.close()
