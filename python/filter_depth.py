import numpy as np
import cv2
import cv
REPEAT = 3
local_samples = 80
neighborhood_global= 60
World_Sampling_Area = 10**5

depth_image = np.load('08-26-21-12-58.npy')

def show_depth(depth):
    depth = depth * 0.05
    depth = depth.clip(0,255)
    depth = depth.astype('uint8')
    cv2.imshow('depth',depth)

def random_point_around(p,h_eta,w_eta):
    import random
    height, width = depth_image.shape
    repeat = REPEAT
    d = 0
    while  (d == 0) and repeat>0 :
        repeat -= 1 
        h = p[0] + random.randint(-h_eta, h_eta)
        w = p[1] + random.randint(-w_eta, w_eta)
        # exceed the border then re-random
        if h<0 or h>height-1 or w<0 or w>width-1:
            continue
        #d = depth_image.item((h,w)) 
        d = 1
    # not able to find
    if repeat==0:
        return 0,0,0
    return h,w,d

def plane_sampling():
    height, width = depth_image.shape
    # select p0,p1,02
    p0 = random_point_around([height/2, width/2,0], height/2, width/2)
    p1 = random_point_around(p0, neighborhood_global, neighborhood_global)
    p2 = random_point_around(p0, neighborhood_global, neighborhood_global)
    # print p0,p1,p2
    z_mean = (p0[2]+p1[2]+p2[2])/3+1# avoid z_mean = 0\
    r_samples = World_Sampling_Area/z_mean 
    # print z_mean, r_samples
    p_list = list()
    p_list.append(p0)
    p_list.append(p1)
    p_list.append(p2)
    for i in range(local_samples-3):
        random_point_around(p0, r_samples, r_samples)
        #p_list.append( random_point_around(p0, r_samples, r_samples) )
    # print len(p_list), p_list   
       
if __name__ == "__main__":
    for i in xrange(20000):
        plane_sampling()
    
    
    #show_depth(depth)
    #cv2.waitKey(0)

