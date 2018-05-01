//
//  FMImageProcessor.m
//  FollowMeMusic
//
//  Created by Collin Lasley on 4/30/18.
//  Copyright © 2018 clasley. All rights reserved.
//

#import "FMImageProcessor.h"

@implementation FMImageProcessor

- (id)init
{
    self = [super init];
    if (self){
        closestQR.distance = 0.0;
        closestQR.data = NULL;
        closestQR.location.x = 0;
        closestQR.location.y = 0;
        
    }
    
    return self;
}

- (double)distance: (FMObjectInformation)obj1 toObject: (FMObjectInformation)obj2
{
    return 0.0;
}

- (FMObjectInformation)parseImage: (cv::Mat &)theImage
{
    return (FMObjectInformation){0,0,0};
}

- (void)showBoxes: (cv::Mat &)theImage withObjData:(void *)objectData personData:(void *)personData
{
    
}

- (void)processImage: (cv::Mat &)theImage
{
    static BOOL firstImage = true;
    cv::Mat workingImage;
    cv::Mat grayscaleImage;
    
    cv::cvtColor(workingImage, grayscaleImage, cv::COLOR_BGR2GRAY);
    cv::GaussianBlur(grayscaleImage, grayscaleImage, {21, 21}, 0.0);
    
    
}

@end
