from dotenv import load_dotenv
import mysql.connector
import os
from datetime import datetime, timedelta, time
from os import system
import pickle
import numpy as np
from PIL import Image, ImageTk
import cv2
import glob
from tkinter import *
from tkinter import messagebox
import PIL.Image
import subprocess
import src.functions_img_processing as functions_img_processing


def load_names(path):
    with open(path, 'rb') as f:
        images = pickle.load(f)
    names = {n: v for n, v in enumerate(images)}
    return names


def mySQLdb_connect():
    load_dotenv()
    sql_password = os.getenv("sql_password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=sql_password,
        database="employees"
    )
    return mydb


def greet(person, reason):
    first_name, last_name = person.split("_")
    title = "Access granted"
    if person == "No_One":
        messagebox.showinfo(message="Person not recognized",
                            title="Access denied")
        system('say Sorry, I did not recognize you')
    else:
        output = {"arrival": 'say Welcome {}, have a nice day!',
                  "departure": 'say Have a good afternoon, {}!'}
        messagebox.showinfo(message="Registered record for {}:\n{} {}".format(
            reason, first_name, last_name), title=title)
        system(output[reason].format(first_name))
    return person


def insert_record_mySQL(cursor, db, person, action, time):
    sql = "INSERT INTO employee_signatures (name, action, time) VALUES (%s, %s, %s)"
    val = ("{}".format(person), "{}".format(action), "{}".format(time))
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "record inserted.")


def most_common(lst):
    return max(set(lst), key=lst.count)


def detect_me(model, face_cascade, names, db, cursor, reason):
    # define global variables
    new_person = {"names": [], "predictions": []}
    current_time = datetime.now()
    # start recording
    video = cv2.VideoCapture(0)
    while True:
        _, frame = video.read()

        # process image
        frame = functions_img_processing.process_image(frame, face_cascade)
        if frame.shape[2] == 1:
            frame = frame/255

            # predict
            print(
                "dimensions frame to model --> {}".format(np.expand_dims(frame, axis=0).shape))
            prediction = model.predict(np.expand_dims(frame, axis=0))[0]
            print(prediction)
            person = [0, 0]
            for n, v in enumerate(prediction):
                if v > person[1]:
                    person = [n, v]
                    """print("{}: {:.2f}%".format(
                        names[person[0]], person[1]*100))
                    print("********")"""
            new_person["names"].append(names[person[0]])
            new_person["predictions"].append(person[1])

            # decide person based on prediction
            if (datetime.now() - current_time).total_seconds() >= 10:
                global the_person
                the_person = most_common(new_person["names"])
                print(new_person)
                print(the_person)

                def Average(lst):
                    return sum(lst) / len(lst)
                percentages_the_person = []
                for i in [index for index, value in enumerate(new_person["names"]) if value == the_person]:
                    percentages_the_person.append(new_person["predictions"][i])
                print(Average(percentages_the_person))
                new_person = []

                # greet the person
                greet(the_person, reason)

                # save frames from person
                directory = "./input/images/{}".format(the_person)
                filename_count = len(
                    glob.glob("./input/images/{}/**".format(the_person)))
                frame_count = 0
                while True and frame_count < 20:
                    filename = "{}_{}".format(the_person, filename_count)
                    _, frame = video.read()
                    frame_count += 1
                    if frame_count % 4 == 0:
                        filename_count += 1
                        im = PIL.Image.fromarray(frame, 'RGB')
                        im.save(os.path.join(
                            directory, filename+".jpg"), "JPEG")
                        # cv2.imshow("Capturing", frame)
                        key = cv2.waitKey(1)
                        if key == ord('q'):
                            break
                    else:
                        pass

                # insert record to mySQL database
                if the_person != "No_One":
                    insert_record_mySQL(cursor, db, the_person,
                                        reason, datetime.now())
                break

            #cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()
    return the_person


def open_mySQLWorkbench():
    subprocess.Popen(["/usr/bin/open", "-W", "-n", "-a",
                      "/Applications/MySQLWorkbench.app"])


def reset_mySQLTable(db, cursor):
    Delete_all_rows = """truncate table employee_signatures"""
    cursor.execute(Delete_all_rows)
    db.commit()
