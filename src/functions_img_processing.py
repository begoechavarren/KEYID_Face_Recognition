import cv2
import os
import glob
import numpy as np
import pickle


def crop_face(image, face_cascade):
    faces_rects = face_cascade.detectMultiScale(
        image, scaleFactor=1.2, minNeighbors=5)
    x, y, w, h = [x for x in faces_rects[0]]
    crop = image[y:y+h, x:x+w]
    img = cv2.resize(crop, (360, 480))
    return img


def fourier_transformation(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    rows, cols = img.shape
    crow, ccol = rows/2, cols/2
    fshift[int(crow-5):int(crow+5), int(ccol-5):int(ccol+5)] = 0
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    return img_back


def process_image(img, face_cascade):
    proc_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    proc_img = cv2.resize(proc_img, None, fx=0.5, fy=0.5)
    proc_img = np.expand_dims(proc_img, axis=2)
    if len(face_cascade.detectMultiScale(proc_img, scaleFactor=1.2, minNeighbors=5)) > 0:
        proc_img = crop_face(proc_img, face_cascade)
        proc_img = fourier_transformation(proc_img)
        proc_img = np.array(cv2.resize(proc_img, (150, 150)))
        proc_img = np.expand_dims(proc_img, axis=2)
        return proc_img
    else:
        return img


def getFrame(sec, name, vidcap, count):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
    hasFrames, image = vidcap.read()
    if not os.path.exists('./input/images/{}'.format(name)):
        os.makedirs('./input/images/{}'.format(name))
    if hasFrames:
        cv2.imwrite("./input/images/{}/{}_".format(name, name) +
                    str(count)+".jpg", image)
    return hasFrames


def video_to_images():
    for video in glob.glob('./input/video/*'):
        vidcap = cv2.VideoCapture(video)
        sec = 0
        frameRate = 0.5
        count = 1
        success = getFrame(sec, video.split(
            '/')[-1].split('.')[0], vidcap, count)
        while success and sec < 35:
            count = count + 1
            sec = sec + frameRate
            sec = round(sec, 2)
            success = getFrame(sec, video.split(
                '/')[-1].split('.')[0], vidcap, count)


def images_to_dict(face_cascade):
    encoding = dict(zip([x.split('/')[-1] for x in glob.glob('./input/images/*')],
                        [x for x in range(len(glob.glob('./input/images/*')))]))
    images = {}
    for name in glob.glob('./input/images/**/*.jpg'):
        persona = name.split('/')[-2]
        img = cv2.imread(name)
        img = process_image(img, face_cascade)
        if img.shape[2] == 1:
            if persona in images:
                images[persona]['images'].append(img)
                images[persona]['names'].append(encoding[persona])
            else:
                images[persona] = {
                    'images': [img],
                    'names': [encoding[persona]]
                }
    return images


def X_y_generator(images):
    images_arrays = {"X": [], "y": []}
    for persona in images:
        images_arrays["X"].append(images[persona]['images'])
        images_arrays["y"].append(images[persona]['names'])
    X = np.concatenate(([e for e in images_arrays['X']]), axis=0)
    y = np.concatenate(([e for e in images_arrays['y']]), axis=0)
    return X, y


def save_images(images):
    with open('./files/images.pickle', 'wb') as f:
        pickle.dump(images, f)
