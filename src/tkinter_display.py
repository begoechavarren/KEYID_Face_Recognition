from tkinter import *
from PIL import ImageTk
import PIL.Image
import src.functions_app as functions_app
import src.new_employee as new_employee
import src.keras_model as keras_model


def tkinter_display(model, face_cascade, names, db, cursor):
    HEIGHT = 500
    WIDTH = 600
    root = Tk()
    root.title("Live Facial Recognition System")
    canvas = Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    # background
    image = PIL.Image.open("./images/background.jpg")
    background_image = ImageTk.PhotoImage(image)
    background_label = Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # title
    label = Label(root, text="KEYID",
                  fg="white", bg='#001b52', width=200)
    label.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
    label.config(font=("Courier", 50))

    # sign here
    label = Label(root, text="Sign here:", fg="white",
                  bg='#001b52', width=200, font="Helvetica 19 bold")
    label.place(relx=0.5, rely=0.25, relwidth=0.75,
                relheight=0.048, anchor='n')

    # button - arrival
    frame = Frame(root, bg='#001b52', bd=5)
    frame.place(relx=0.3125, rely=0.3, relwidth=0.375,
                relheight=0.1, anchor='n')

    button = Button(frame, text="Arrival", font="Helvetica 19 bold", command=lambda: functions_app.detect_me(
        model, face_cascade, names, db, cursor, "arrival"))
    button.place(relx=0, relheight=1, relwidth=1)
    button.configure(foreground='#001b52', relief='solid')

    # button - departure
    frame = Frame(root, bg='#001b52', bd=5)
    frame.place(relx=0.6875, rely=0.3, relwidth=0.375,
                relheight=0.1, anchor='n')

    button = Button(frame, text="Departure", font="Helvetica 19 bold", command=lambda: functions_app.detect_me(
        model, face_cascade, names, db, cursor, "departure"))
    button.place(relx=0, relheight=1, relwidth=1)
    button.configure(foreground='#001b52', relief='solid')

    # separator
    label = Label(root, bg='#001b52', width=200)
    label.place(relx=0.5, rely=0.45, relwidth=0.75,
                relheight=0.002, anchor='n')

    # button - register new employee
    frame = Frame(root, bg='#001b52', bd=5)
    frame.place(relx=0.5, rely=0.50, relwidth=0.75, relheight=0.08, anchor='n')

    button = Button(frame, text="► Register new employee",
                    font="Helvetica 19 bold", command=lambda: new_employee.ask_name())
    button.place(relx=0, relheight=1, relwidth=1)
    button.configure(foreground='#001b52', relief='solid')

    # button - update system
    frame = Frame(root, bg='#001b52', bd=5)
    frame.place(relx=0.5, rely=0.6, relwidth=0.75, relheight=0.08, anchor='n')

    button = Button(frame, text="► Update system",
                    font="Helvetica 19 bold", command=lambda: keras_model.train_model(face_cascade))
    button.place(relx=0, relheight=1, relwidth=1)
    button.configure(foreground='#001b52', relief='solid')

    # button - open signatures database
    frame = Frame(root, bg='#001b52', bd=5)
    frame.place(relx=0.5, rely=0.7, relwidth=0.75, relheight=0.08, anchor='n')

    button = Button(frame, text="► Open signatures database",
                    font="Helvetica 19 bold", command=lambda: functions_app.open_mySQLWorkbench())
    button.place(relx=0, relheight=1, relwidth=1)
    button.configure(foreground='#001b52', relief='solid')

    # button - reset signatures database
    frame = Frame(root, bg='#001b52', bd=5)
    frame.place(relx=0.5, rely=0.8, relwidth=0.75, relheight=0.08, anchor='n')

    button = Button(frame, text="► Reset signatures database",
                    font="Helvetica 19 bold", command=lambda: functions_app.reset_mySQLTable(db, cursor))
    button.place(relx=0, relheight=1, relwidth=1)
    button.configure(foreground='#001b52', relief='solid')

    # logo
    img = ImageTk.PhotoImage(PIL.Image.open("./images/logo_white.png"))
    label = Label(root, image=img, bg='#001b52')
    label.place(relx=0.82, rely=0.1, relwidth=0.1, relheight=0.1, anchor='n')

    root.mainloop()
