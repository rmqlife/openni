import numpy as np
import cv2
#CV_CAP_OPENNI = 910
cap = cv2.VideoCapture(910)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
		# Display the resulting frame
        frame = frame * 0.05
        frame = frame.clip(0,255)
        frame = frame.astype('uint8')
        
        frame[frame>60] = 0
        cv2.imshow('frame',frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break


        #print np.amax(frame) #9000 5000
        #print np.amin(frame) #0
# When everything done, release the capture
# np.savetxt('frame.txt',frame,fmt='%.1f')
cap.release()
cv2.destroyAllWindows()
