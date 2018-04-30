//
//  ViewController.m
//  FollowMeMusic
//
//  Created by Collin Lasley on 4/11/18.
//  Copyright © 2018 clasley. All rights reserved.
//

#import "ViewController.h"

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    videoCamera = [[CvVideoCamera alloc] initWithParentView:cameraImageView];
    [videoCamera setDelegate:self];
    videoCamera.defaultAVCaptureDevicePosition = AVCaptureDevicePositionFront;
    videoCamera.defaultAVCaptureSessionPreset = AVCaptureSessionPreset352x288;
    videoCamera.defaultAVCaptureVideoOrientation = AVCaptureVideoOrientationPortrait;
    videoCamera.defaultFPS = 30;
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)dankButtonPressed: (id)sender
{
    [videoCamera start];
}

- (void)processImage:(cv::Mat&)theImage
{
    cv::Mat imageWorkingCopy;
    cv::cvtColor(theImage, imageWorkingCopy, CV_BGRA2BGR);
    
    cv::bitwise_not(imageWorkingCopy, imageWorkingCopy);
    cv::cvtColor(imageWorkingCopy, theImage, CV_BGR2BGRA);
}

@end
