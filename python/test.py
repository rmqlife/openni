import numpy as np
import cv2
import cv

def show_im(gray, depth):
    depth = depth * 0.05
    depth = depth.clip(0,255)
    depth = depth.astype('uint8')
    
    gray[depth>100] = 0
    gray[depth==0] = 0
    
    show = np.concatenate((depth, gray), axis=1)
    cv2.imshow('depth and gray',show)


if __name__ == "__main__":
    # detection init
    face_cascade = cv2.CascadeClassifier('/home/rmqlife/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
    
    
    cap = cv2.VideoCapture(cv.CV_CAP_OPENNI_ASUS)
    while(True):
        # Capture frame-by-frame
        cap.grab()
        ret1, depth = cap.retrieve(None,cv.CV_CAP_OPENNI_DEPTH_MAP)
        ret2, bgr = cap.retrieve(None,cv.CV_CAP_OPENNI_BGR_IMAGE)
        if ret1 and ret2:
            gray = cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY)
            #gray[depth>1000] = 0
            #gray[depth==0] = 0
            
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(bgr, (x,y), (x+w, y+h), (255,0,0), 2)
            
            cv2.imshow('gray', gray)
            
            #bgr[depth==0] = [212,175,123]
            #bgr[depth>1000] = [212,175,123]
            cv2.imshow('BGR', bgr)
            
            
        key = cv2.waitKey(30)
        if key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
