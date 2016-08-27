import numpy as np
import cv2
import cv

def show_depth(depth):
    depth = depth * 0.05
    depth = depth.clip(0,255)
    depth = depth.astype('uint8')
    cv2.imshow('depth',depth)

def random_point(arr):
    import random
    height,width = arr.shape
    # print height,width
    h = random.randrange(height)
    w = random.randrange(width)
    # print h,w
    return h,w,arr[h][w]

def random_point_around(arr,p,eta):
    import random
    height, width = arr.shape
    h = p[0] + random.randint(-eta, eta)
    w = p[1] + random.randint(-eta, eta)
    h = np.clip(h,0,height-1)
    w = np.clip(w,0,width-1)
    return h,w,arr[h,w] 
    
if __name__ == "__main__":
    depth = np.load('08-26-21-12-58.npy')
    p0 = random_point(depth)
    p1 = random_point_around(depth,p0,10)
    p2 = random_point_around(depth,p0,10)
    print p0,p1,p2
    
    
    
    #show_depth(depth)
    #cv2.waitKey(0)

