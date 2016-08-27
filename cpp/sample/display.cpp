#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>

using namespace cv;
using namespace std;

int threshNear = 60;
int threshFar = 100;
int dilateAmt = 1;
int erodeAmt = 1;
int blurAmt = 1;
int blurPre = 1;
void on_trackbar(int, void*){}

int main() {
    VideoCapture capture;
    capture.open(CV_CAP_OPENNI);
    if( !capture.isOpened() )
    {
        cout << "Can not open a capture object." << endl;
        return -1;
    }
    cout << "ready" << endl;
    vector<vector<Point> > contours;
    namedWindow("depth map");
    createTrackbar( "amount dilate", "depth map", &dilateAmt,16, on_trackbar );
    createTrackbar( "amount erode", "depth map", &erodeAmt,16, on_trackbar );
    createTrackbar( "amount blur", "depth map", &blurAmt,16, on_trackbar );
    createTrackbar( "blur pre", "depth map", &blurPre,1, on_trackbar );
    createTrackbar( "threshold near", "depth map", &threshNear,255, on_trackbar );
    createTrackbar( "threshold far", "depth map", &threshFar,255, on_trackbar );
    for(;;)
    {
        Mat depthMap;
        if( !capture.grab() )
        {
            cout << "Can not grab images." << endl;
            return -1;
        }
        else
        {
            if( capture.retrieve( depthMap, CV_CAP_OPENNI_DEPTH_MAP ) )
            {
                const float scaleFactor = 0.05f;
                Mat show; depthMap.convertTo( show, CV_8UC1, scaleFactor );
                //threshold
                Mat tnear,tfar;
                show.copyTo(tnear);
                show.copyTo(tfar);
                threshold(tnear,tnear,threshNear,255,CV_THRESH_TOZERO);
                threshold(tfar,tfar,threshFar,255,CV_THRESH_TOZERO_INV);
                show = tnear & tfar;//or cvAnd(tnear,tfar,show,NULL); to join the two thresholded images
                //filter
                if(blurPre == 1) blur(show,show,Size(blurAmt+1,blurAmt+1));
                Mat cntr; show.copyTo(cntr);
                erode(cntr,cntr,Mat(),Point(-1,-1),erodeAmt);
                if(blurPre == 0) blur(cntr,cntr,Size(blurAmt+1,blurAmt+1));
                dilate(cntr,cntr,Mat(),Point(-1,-1),dilateAmt);

                //compute and draw contours
                findContours(cntr,contours,0,1);
                drawContours(cntr,contours,-1,Scalar(192,0,0),2,3);

                //optionally compute bounding box and circle to exclude small blobs(non human) or do further filtering,etc.
                int numContours = contours.size();
                vector<vector<Point> > contours_poly( numContours );
                vector<Rect> boundRect( numContours );
                vector<Point2f> centers( numContours );
                vector<float> radii(numContours);
                for(int i = 0; i < numContours; i++ ){
                    approxPolyDP( Mat(contours[i]), contours_poly[i], 3, true );
                    boundRect[i] = boundingRect( Mat(contours_poly[i]) );
                    minEnclosingCircle(contours_poly[i],centers[i],radii[i]);
                    rectangle( cntr, boundRect[i].tl(), boundRect[i].br(), Scalar(64), 2, 8, 0 );
                    circle(cntr,centers[i],radii[i],Scalar(192));
                 }

                imshow( "depth map", show );
                imshow( "contours", cntr );
            }

        }

        if( waitKey( 30 ) == 27 ) break;//exit on esc
    }
}

