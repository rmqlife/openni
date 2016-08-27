import numpy as np
import cv2
import cv

def show_depth(depth):
    depth = depth * 0.05
    depth = depth.clip(0,255)
    depth = depth.astype('uint8')
    cv2.imshow('depth',depth)


if __name__ == "__main__":
    cap = cv2.VideoCapture(cv.CV_CAP_OPENNI_ASUS)
    while(True):
        # Capture frame-by-frame
        cap.grab()
        ret1, depth = cap.retrieve(None,cv.CV_CAP_OPENNI_DEPTH_MAP)
        ret2, bgr = cap.retrieve(None,cv.CV_CAP_OPENNI_BGR_IMAGE)
        if ret1 and ret2:
            gray = cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY)
            show_depth(depth)
            #cv2.imshow('BGR', bgr)
        key = cv2.waitKey(30)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('c'):
            import datetime
            timestamp = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")
            np.save(timestamp+'.npy', depth)          
            if cv2.imwrite(timestamp+".png", bgr):
                print "captured at "+ timestamp
                
    cap.release()
    cv2.destroyAllWindows()
