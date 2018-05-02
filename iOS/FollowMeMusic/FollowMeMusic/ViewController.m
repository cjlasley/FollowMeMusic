//
//  ViewController.m
//  FollowMeMusic
//
//  Created by Collin Lasley on 4/11/18.
//  Copyright © 2018 clasley. All rights reserved.
//

#import "ViewController.h"
#import "FMNetwork.h"

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    videoCamera = [[CvVideoCamera alloc] initWithParentView:cameraImageView];
    [videoCamera setDelegate:self];
    videoCamera.defaultAVCaptureDevicePosition = AVCaptureDevicePositionBack;
    videoCamera.defaultAVCaptureSessionPreset = AVCaptureSessionPreset3840x2160;
    videoCamera.defaultAVCaptureVideoOrientation = AVCaptureVideoOrientationPortrait;
    videoCamera.defaultFPS = 30;
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)dankButtonPressed: (id)sender
{
    NSString *filePath;
    
    [videoCamera start];
    filePath = [[NSBundle mainBundle] pathForResource:@"InsultTwoPanelTwo" ofType:@"jpg"];
    FMNetwork *uploader = [[FMNetwork alloc] initWithURL:[NSURL URLWithString:@"http://172.20.10.2:5000/upload"] filePath:filePath delegate:self doneCallback:@selector(onUploadDone) errorCallback:@selector(onUploadError)];
}

-  (void)onUploadDone
{
    printf("Upload is done!\n");
}

- (void)onUploadError
{
    printf("Upload encountered an error!\n");
}

- (void)processImage:(cv::Mat&)theImage
{
    cv::Mat imageWorkingCopy;
    cv::cvtColor(theImage, imageWorkingCopy, CV_BGRA2BGR);
    
    //cv::bitwise_not(imageWorkingCopy, imageWorkingCopy);
    cv::cvtColor(imageWorkingCopy, theImage, CV_BGR2BGRA);
}

@end
