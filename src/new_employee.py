import glob
import os
import cv2
import PIL.Image
from tkinter.simpledialog import askstring


def capture_images(name):
    directory = "./input/images/{}".format(name)
    os.makedirs(directory, exist_ok=True)

    filename_count = len(
        glob.glob("./input/images/{}/**".format(name)))
    frame_count = 0

    video = cv2.VideoCapture(0)

    while True:
        filename = "{}_{}".format(name, filename_count)
        _, frame = video.read()
        frame_count += 1
        if frame_count < 300:
            if frame_count % 5 == 0:
                filename_count += 1
                im = PIL.Image.fromarray(frame, 'RGB')
                im.save(os.path.join(directory, filename+".jpg"), "JPEG")
                #cv2.imshow("Capturing", frame)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
            else:
                pass
        else:
            break
    video.release()
    cv2.destroyAllWindows()


def ask_name():
    name = askstring('New Record', 'What is your name?')
    capture_images(name)
