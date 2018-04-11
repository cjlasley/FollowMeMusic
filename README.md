# Follow Me Music
An OpenCV project where servos with speakers attached to them turn to track people in the room.

___

## MVP:
* Single Bluetooth speaker
* Interfaces with Python code on Mac
* Only controls volume via distance


### Continuing
* Interface with Amazon Alexa for multiple speaker control
* Build IOS and Android apps that have OpenCV on them, use them as camera to track distance

### Epic:
* Integrate with Raspberry Pi
* Have Pi control servos and turn servos towards the person each is tracking


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
