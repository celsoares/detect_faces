import cv2
import mediapipe as mp
import time
import os
from threading import Thread

def fala(som):
    os.system(som)


img=cv2.VideoCapture(0)

model=mp.solutions.face_detection

face=model.FaceDetection()
desenho=mp.solutions.drawing_utils
fase=0
t_ref=time.time()
while True:

    ret, frame = img.read()

    if not ret: break


    face_list=face.process(frame)

#caso detetar cara na camara
    if face_list.detections:
        
        #1ª vez que deteta a cara
        if (fase==0):
          fase=1
          Thread(target=fala("1.mp3")).start()
          t_ref=time.time()

        # Depois de 10s a detetar prepara a foto
        if fase==1 and (time.time()-t_ref>10):
            fase=2
            Thread(target=fala("2.mp3")).start()
            t_ref=time.time()
        
        # Depois de 7s contagem decrescente
        if fase==2 and (time.time()-t_ref>3):
            fase=3
            t_ref=time.time()
        
        if fase==3:
            if (time.time()-t_ref)<1: count=5
            elif (time.time()-t_ref)<2: count=4
            elif (time.time()-t_ref)<3: count=3
            elif (time.time()-t_ref)<4: count=2
            elif (time.time()-t_ref)<5: count=1
            elif time.time()-t_ref<6: fase=4
            if fase==3: frame=cv2.putText(frame, f"{count}", (250,250), cv2.FONT_HERSHEY_SIMPLEX, 10, (255,0,0), 5)

        # Grava a imagem
        if fase==4:
            Thread(target=fala("3.mp3")).start()
            cv2.imwrite("cap.jpg", frame)
            time.sleep(2)
            fase=5
            t_ref=time.time()
        
        # reinicia ao fim de 5
        
        if fase==5 and time.time()-t_ref>5: fase=0

        


        for x in face_list.detections:
            #print(x)
            #cv2.rectangle(frame, (x,y),(x+w, y+h), (255, 0 , 0), 1 )
            desenho.draw_detection(frame, x)
    else:
        if time.time()-t_ref>10 and fase!=0:
            print("reinicio!!!")
            fase=0

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) == 27:
        break

img.release()
cv2.destroyAllWindows()