# Follow Me Music
An OpenCV project where servos with speakers attached to them turn to track people in the room.
___

## MVP:
* Single Bluetooth speaker
* Interfaces with Python code on Mac
* Only controls volume via distance

### Continuing:
* Interface with Amazon Alexa for multiple speaker control
* Build IOS and Android apps that have OpenCV on them, use them as camera to track distance

### Epic:
* Integrate with Raspberry Pi
* Have Pi control servos and turn servos towards the person each is tracking

### [ZenHub Kanban Board](https://app.zenhub.com/workspace/o/cjlasley/followmemusic/boards?repos=129161238)

### Dependencies:

#### Mac:
The Mac version can run off the pure core algorithm Python script and requires the following external dependencies:
- Python3.6 or greater
- opencv2
- pyzbar
- imutils <- included with the brew opencv package
- osascript

These can be installed as follows with pip and homebrew:
```sh 
brew install opencv@2
pip install osascript
pip install pyzbar
```

### Development:

#### Core Algorithm:
The core algorithm consists of a Python script that uses the openCV and zBar libraries to detect, locate, and read a QR code and then find the distance between this and a detected moving object. Motion detection is done by subtracting two subsequent frames and then applying filters to get the longest changing contour lines. The average cumulative midpoint of all of the boxes around the contours are used as the center point of the moving object. At this point, a 2 dimensional distance can be obtained between the QR code and detected object. However, since these exist in a 3 dimensional plane, the Z-distance to both objects are also obtained. This is done by using knowledge of the focal length and sensor height of the camera and then getting a ratio of the actual size (or estimated actual size) of the QR code and human compared to their perceived size in the picture. With all 3 dimensions now obtained, a 3 dimensional distance between the two objects can be calculated and the nearest QR code is given a red dot in its center, as shown below.
<div style="text-align:center">
<img src="README_Media/qrToMovementTracking.gif" width=300></img>
</div>

## Technical
* Apps for IOS and Android will be developed using Flutter, a Dart based mobile development API
  > Check out [Flutter's homepage](https://flutter.io/) for more information
* OpenCV has native support for Objective-C, which can be used as an alternative development approach to IOS apps
  > Reference [OpenCV video processing with Objective-C](https://docs.opencv.org/2.4/doc/tutorials/ios/video_processing/video_processing.html) for documentation


### Installation
* You will need to do the following:
1. Install Flutter:

    > [Windows](https://flutter.io/setup-windows/)
    >
    > [Mac](https://flutter.io/setup-macos/)
    >
    > [Linux](https://flutter.io/setup-linux/#update-your-path)

2. Download Android Studio:

    > [Windows | Mac | Linux](https://developer.android.com/studio/index.html#downloads)

  2.1 You may be prompted to install NTK and CMAKE after you create your first project


### Helpful Tips/Resources
* Android device emulation can be performed within Android Studio, so you do not need a physical device to test basic app        features. However, keep in mind that we will be using a series of image bounding boxes to measure distances, which may require a physical device to use the camera. I haven't looked into this yet. The other method would be to have a sequence of images preloaded onto the emulator that OpenCV could process.
    > Check out the [Create and Manage Virtual Devices](https://developer.android.com/studio/run/managing-avds.html) documentation for more device emulation details

* OpenCV integration with Flutter [Custom Platform](https://flutter.io/platform-channels/)
* OpenCV for [IOS](https://docs.opencv.org/2.4/doc/tutorials/ios/video_processing/video_processing.html)
