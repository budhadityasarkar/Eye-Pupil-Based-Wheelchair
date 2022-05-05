import cv2
import dlib
import utils
from keras.models import load_model
import numpy as np
import serial
import time

bluetooth=serial.Serial('COM4', 9600)  # Start communications with the bluetooth unit
print("Connected")
bluetooth.flushInput()  # This gives the bluetooth a little kick


cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
model = load_model('Eye-detect-model\content\Eye-detect-model')
eye_model = load_model('eyeprojectmodel.h5')

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.imwrite('./saved/frame.jpg', frame)
    path = './saved/frame.jpg'
    if ret:
        face = utils.face_detection(path)
        flag=" "
        # print(cords)
        if face is not None:
            utils.draw_rectangle(path, face)
            utils.eye_detecton(path, face)

            left_eye = cv2.imread('eye\Left\Left_eye.jpg')
            # left_eye = cv2.cvtColor(left_eye, cv2.COLOR_BGR2GRAY)
            right_eye = cv2.imread('eye\Right\Right_eye.jpg')
            # right_eye = cv2.cvtColor(right_eye, cv2.COLOR_BGR2GRAY)

            # print(left_eye.shape)
            # print(right_eye.shape)

            left_eye = np.expand_dims(left_eye, axis=0)
            right_eye = np.expand_dims(right_eye, axis=0)


            # print(left_eye.shape)
            # print(right_eye.shape)

            left_eye_pred = model.predict(left_eye)
            right_eye_pred = model.predict(right_eye)
            

            if (left_eye_pred+right_eye_pred)/2 > 0.5:
                img = cv2.imread("saved/frame.jpg")
                flag=utils.predict()
                cv2.putText(img, flag,(300,30) , cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.imwrite("saved/frame.jpg", img)

                print("Ping")
                print(flag)
                if flag== "forward":
                    i=1
                    bluetooth.write(b"BOOP "+str.encode(str(i)))  # These need to be bytes not unicode, plus a number
                elif flag== "left":
                    i=2
                    bluetooth.write(b"BOOP "+str.encode(str(i)))
                
                else:
                    i=3
                    bluetooth.write(b"BOOP "+str.encode(str(i)))

               
                
                #print('Left Eye Prediction: ',eye_model.predict(leye))
                #print('Right Eye prediction',eye_model.predict(reye))
            else:
                flag="stop"
                i=4
                bluetooth.write(b"BOOP "+str.encode(str(i)))
                print(flag)

        else:
            img = cv2.imread('./saved/frame.jpg')
            cv2.putText(img, 'No face detected', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imwrite(path, img)
        cv2.imshow('camera', cv2.imread('./saved/frame.jpg'))

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
