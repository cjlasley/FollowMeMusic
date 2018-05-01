//
//  FMImageProcessor.h
//  FollowMeMusic
//
//  Created by Collin Lasley on 4/30/18.
//  Copyright © 2018 clasley. All rights reserved.
//

#include <opencv2/opencv.hpp>
#include <opencv2/videoio/cap_ios.h>
#import <Foundation/Foundation.h>
#include <UIKit/UIKit.h>

#include <math.h>

typedef struct{
    double x;
    double y;
    double z;
}FMObjectInformation;

@interface FMImageProcessor : NSObject
{
    NSMutableArray *closestQR;
    UIColor        *lineColor;
    UIColor        *closestColor;
    UIColor        *personColor;
    
    NSUInteger actualQRHeight;
    double     focalLength;
    double     sensorHeight;
    NSUInteger avgPersonHeight;
    NSUInteger minContourSize;
    
}

- (double)distance: (FMObjectInformation)obj1 toObject: (FMObjectInformation)obj2;

- (FMObjectInformation)parseImage: (cv::Mat &)theImage;

- (void)showBoxes: (cv::Mat &)theImage withObjData:(void *)objectData personData:(void *)personData;

- (void)processImage: (cv::Mat &)theImage;

@end
