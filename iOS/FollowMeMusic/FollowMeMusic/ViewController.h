//
//  ViewController.h
//  FollowMeMusic
//
//  Created by Collin Lasley on 4/11/18.
//  Copyright © 2018 clasley. All rights reserved.
//

#include <opencv2/opencv.hpp>
#include <opencv2//videoio/cap_ios.h>
#import <UIKit/UIKit.h>

@interface ViewController : UIViewController<CvVideoCameraDelegate>
{
    IBOutlet UIImageView *cameraImageView;
    IBOutlet UIButton    *dankButton;
    UISlider             *volumeControlSlider;
    
    CvVideoCamera *videoCamera;
}

- (IBAction)dankButtonPressed: (id)sender;


@end
