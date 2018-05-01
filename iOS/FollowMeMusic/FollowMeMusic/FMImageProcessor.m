//
//  FMImageProcessor.m
//  FollowMeMusic
//
//  Created by Collin Lasley on 4/30/18.
//  Copyright © 2018 clasley. All rights reserved.
//

#import "FMImageProcessor.h"

@implementation FMImageProcessor

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
    
}

@end
