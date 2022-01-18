import os
import glob
import face_recognition
import cv2
import imutils
import numpy as np
import time
from djitellopy import tello
import jovian

tello = tello.Tello()
tello.connect()
print(tello.get_battery())
tello.streamon()

def send_email():
    myPath = glob.glob('C:\\Users\\Irfan Mazuki\\Documents\\File\\BSE\\SEM 7\\WIF3008 REAL TIME SYSTEM\\Group Project\\codes\\Billy-20211229\\Billy\\intruders\\*')
    global countFolder
    count = 0
    # if(len(myPath)<20):
    #     moduleVal = 2
    # else:
    #     moduleVal = 4
    for i in myPath:
        img = cv2.imread(i)
        #     cap.set(3, 640)
        #     cap.set(4, 480)
        #     cap.set(10,180)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.Laplacian(gray_img, cv2.CV_64F).var()
        if (count % 1 == 0 and blur > 320):
            cv2.imwrite(
                "C:\\Users\\Irfan Mazuki\\Documents\\File\\BSE\\SEM 7\\WIF3008 REAL TIME SYSTEM\\Group Project\\codes\\Billy-20211229\\Billy\\saved\\pic-{}.jpg".format(
                    count), img)
            count += 1

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from datetime import datetime
    #  For advanced mails and attachment files.
    username = "bluearseus@gmail.com"
    passwd = "rts777drone"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    # server = smtplib.SMTP(smtphost)
    server.ehlo()
    server.starttls()
    server.login(username, passwd)
    # server.sendmail(username, 'irfanmazuki9@gmail.com', "TEST")
    print('success')
    msg = MIMEMultipart()
    msg['from'] = username
    msg['to'] = 'irfanmazuki9@gmail.com'
    tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
    msg['subject'] = "Intruders Images at " + str(tm)
    text = "Unknown individual detected. Check out the image attached."
    msg.attach(MIMEText(text))
    F = glob.glob("C:\\Users\\Irfan Mazuki\\Documents\\File\\BSE\\SEM 7\\WIF3008 REAL TIME SYSTEM\\Group Project\\codes\\Billy-20211229\\Billy\\intruders\\*")
    for i in F:
        with open(i, 'rb') as f:
            part = MIMEApplication(f.read())
            part.add_header('content-Disposition', 'attachment', filename='{}.jpg'.format(count + 1))
            msg.attach(part)
    server.sendmail(username, 'irfanmazuki9@gmail.com', msg.as_string())

paths = glob.glob('C:\\Users\\Irfan Mazuki\\Documents\\File\\BSE\\SEM 7\\WIF3008 REAL TIME SYSTEM\\Group Project\\codes\\Billy-20211229\\Billy\\data\\*')
names = []
images = []
image_encodings = []
image_names = []
count_img = 0
for i in paths:
    images.append(face_recognition.load_image_file(i))
    image_encodings.append(face_recognition.face_encodings(images[count_img])[0])
    image_names.append(i.split('\\')[-1].split('.')[0])
    count_img+=1
    print(image_names)

# host = ''
# port = 9000
# local_address = (host, port)
# drone = tello.Tello(host, port)
# # Put Tello into command mode
# drone.send("command", 3)
# # Send the takeoff command
# drone.send("takeoff", 10)

count = 0
# frame_read = drone.get_frame_read()

while True:
    frame = tello.get_frame_read().frame
    frame = imutils.resize(frame, width=400)

    gray = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(gray)
    face_encodings = face_recognition.face_encodings(gray, face_locations)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(image_encodings, face_encoding)
        name = 'Unknown'
        face_distances = face_recognition.face_distance(image_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = image_names[best_match_index]
        if(name=='Unknown'):
            cv2.imwrite('C:\\Users\\Irfan Mazuki\\Documents\\File\\BSE\\SEM 7\\WIF3008 REAL TIME SYSTEM\\Group Project\\codes\\Billy-20211229\\Billy\\intruders\\intru-{}.jpg'.format(count),frame)
            count+=1
            send_email()
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 3)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    cv2.imshow('Tello detection...', frame)
    clearFolder = glob.glob('C:\\Users\\Irfan Mazuki\\Documents\\File\\BSE\\SEM 7\\WIF3008 REAL TIME SYSTEM\\Group Project\\codes\\Billy-20211229\\Billy\\intruders\\*')
    for f in clearFolder:
        os.remove(f)
    #change the frame per ms
    if cv2.waitKey(1) == ord('q'):
        break

# Stop the BackgroundFrameRead and land the drone
drone.end()
cv2.destroyAllWindows()
