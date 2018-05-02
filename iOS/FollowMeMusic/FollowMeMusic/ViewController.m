//
//  ViewController.m
//  FollowMeMusic
//
//  Created by Collin Lasley on 4/11/18.
//  Copyright © 2018 clasley. All rights reserved.
//

#import "ViewController.h"
#import "FMNetwork.h"

static BOOL shouldSend = NO;

static NSMutableArray *senderArray;

#define AntiARCRetain(...) void *retainedThing = (__bridge_retained void *)__VA_ARGS__; retainedThing = retainedThing
#define AntiARCRelease(...) void *retainedThing = (__bridge void *) __VA_ARGS__; id unretainedThing = (__bridge_transfer id)retainedThing; unretainedThing = nil

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    senderArray = [[NSMutableArray alloc] init];
    videoCamera = [[CvVideoCamera alloc] initWithParentView:cameraImageView];
    [videoCamera setDelegate:self];
    videoCamera.defaultAVCaptureDevicePosition = AVCaptureDevicePositionBack;
    videoCamera.defaultAVCaptureSessionPreset = AVCaptureSessionPreset3840x2160;
    videoCamera.defaultAVCaptureVideoOrientation = AVCaptureVideoOrientationPortrait;
    videoCamera.defaultFPS = 4;
    
    //MPVolumeView *aView = [[MPVolumeView alloc] initWithFrame:[volumeSlider frame]];
    //[((id)aView) _commitVolumeChange];
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)dankButtonPressed: (id)sender
{
    NSString *filePath;
    static BOOL firstTime = YES;
    
    [videoCamera start];
    //filePath = [[NSBundle mainBundle] pathForResource:@"InsultTwoPanelTwo" ofType:@"jpg"];
    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *directory = [paths objectAtIndex:0];
    filePath = [directory stringByAppendingPathComponent:[NSString stringWithFormat:@"img.jpg"]];
    
    if (firstTime) {
        firstTime = NO;
    }else{
        shouldSend = YES;
    }
    //FMNetwork *uploader = [[FMNetwork alloc] initWithURL:[NSURL URLWithString:@"http://172.20.10.2:5000/upload"] filePath:filePath delegate:self doneCallback:@selector(onUploadDone) errorCallback:@selector(onUploadError)];
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
    static BOOL firstTime = NO;
    
    if (/*!firstTime &&*/ shouldSend){
        firstTime = YES;
        //shouldSend = NO;
    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *directory = [paths objectAtIndex:0];
    NSString *filePath = [directory stringByAppendingPathComponent:[NSString stringWithFormat:@"img.jpg"]];
    const char* filePathC = [filePath cStringUsingEncoding:NSMacOSRomanStringEncoding];
    
    const cv::String thisPath = (const cv::String)filePathC;
    
    //Save image
    imwrite(thisPath, theImage);
    
    FMNetwork *uploader = [[FMNetwork alloc] initWithURL:[NSURL URLWithString:@"http://172.20.10.2:5000/upload"] filePath:filePath delegate:self doneCallback:@selector(onUploadDone) errorCallback:@selector(onUploadError)];
    }
    
    //cv::bitwise_not(imageWorkingCopy, imageWorkingCopy);
    cv::cvtColor(imageWorkingCopy, theImage, CV_BGR2BGRA);
}

@end
