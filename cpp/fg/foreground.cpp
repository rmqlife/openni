#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>

using namespace cv;
using namespace std;

int threshNear = 0;
int threshFar = 60;

void on_trackbar(int, void*){}
int main() {
    VideoCapture capture;
    capture.open(CV_CAP_OPENNI);
    if( !capture.isOpened() ){
        cout << "Can not open a capture object." << endl;
        return -1;
    }
    namedWindow("depth map");
    createTrackbar( "threshold near", "depth map", &threshNear, 255, on_trackbar );
    createTrackbar( "threshold far", "depth map", &threshFar, 255, on_trackbar );
    while(true){
        Mat depthMap;
        if( !capture.grab() ){
            cout << "Can not grab images." << endl;
            return -1;
        }
        else {
            if(capture.retrieve(depthMap, CV_CAP_OPENNI_DEPTH_MAP) ){
                const float scaleFactor = 0.05f;
                Mat show; 
                depthMap.convertTo( show, CV_8UC1, scaleFactor );
                //threshold
                Mat tnear,tfar;
                show.copyTo(tnear);
                show.copyTo(tfar);
                threshold(tnear,tnear,threshNear,255,CV_THRESH_TOZERO);
                threshold(tfar,tfar,threshFar,255,CV_THRESH_TOZERO_INV);
                show = tnear & tfar;//or cvAnd(tnear,tfar,show,NULL); to join the two thresholded images
                imshow( "depth map", show );
            }
            if (capture.retrieve(cam,  CV_CAP_OPENNI_DEPTH_MAP) ) {
                
            }
        }
        if(waitKey( 30 )  == 27 ) 
            break;//exit on esc
    }
    capture.release();
    destroyAllWindows();
}

