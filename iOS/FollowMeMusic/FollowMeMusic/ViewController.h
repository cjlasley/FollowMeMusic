//
//  ViewController.h
//  FollowMeMusic
//
//  Created by Collin Lasley on 4/11/18.
//  Copyright © 2018 clasley. All rights reserved.
//

#include "FMImageProcessor.h"
#import <UIKit/UIKit.h>

@interface ViewController : UIViewController<CvVideoCameraDelegate>
{
    IBOutlet UIImageView *cameraImageView;
    IBOutlet UIButton    *dankButton;
    
    CvVideoCamera *videoCamera;
}

- (IBAction)dankButtonPressed: (id)sender;


@end

