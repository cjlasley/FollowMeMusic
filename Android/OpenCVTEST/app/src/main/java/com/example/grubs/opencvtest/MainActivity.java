/*
    MainActivity.java
    Tristan Van Cise
    Software Construction Project 3
    04/28/2018
    Backend for FollowMeMusic
 */

package com.example.grubs.opencvtest;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Camera;
import android.graphics.Color;
import android.media.AudioManager;
import android.net.Uri;
import android.os.Environment;
import android.os.Parcel;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.SurfaceView;
import android.widget.ImageView;
import android.widget.Toast;
import android.view.View;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraManager;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.JavaCameraView;
import org.opencv.android.OpenCVLoader;
import org.opencv.android.Utils;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import static org.opencv.imgproc.Imgproc.boundingRect;
import static org.opencv.imgproc.Imgproc.getDerivKernels;

// Needed for OpenCV Camera
public class MainActivity extends AppCompatActivity implements CameraBridgeViewBase.CvCameraViewListener2 {

    private static final String TAG = "MainActivity";

    static {
        if(!OpenCVLoader.initDebug()) {
            Log.d(TAG, "OpenCV not loaded");
        } else {
            Log.d(TAG, "OpenCV loaded");
        }
    }

    // OpenCV Camera Variables:
    CameraBridgeViewBase cameraBridgeViewBase;

    // A Mat stores data about an image in a matrix with a specified format
    // usually the syntax is Mat(width, height, <format>) where <format> can
    // be rgb, rgba, etc. Because Mats are large data structures, open CV
    // handles them using references to the DATA, but changes the HEADERS as
    // needed. This allows modifications to be made to a resource without affecting
    // the actual data, since ~all transformation are stored in the header~.
    Mat mat1, mat2, mat3, frame, previousFrame;
    Boolean first = true;
    BaseLoaderCallback baseLoaderCallback; // Callback interface for OpenCV libraries

    /* Images */
    ImageView imageView;
    Uri imageUri;
    int nFrames = 1;
    static int mainContourSize = 500;
    int frameCount = 0;

        /* Grayscaling */
        Bitmap grayBitmap, imageBitmap;

    /* Audio Adjusting */
    AudioManager audio;
    int currentVolume;
    int maxVolume;
    float percentageOfMaxVolume;

    /* Bluetooth */
//    BluetoothAdapter bluetoothAdapter;
//    ArrayList<BluetoothDevice> discoveredDevices = new ArrayList<>();
//    BluetoothSocket socket = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // OpenCV Check - Toast popup
        if(OpenCVLoader.initDebug()) {
            Toast.makeText(getApplicationContext(), "OpenCV loaded in successfully", Toast.LENGTH_LONG).show();

            // Open CV Camera:
            cameraBridgeViewBase = (JavaCameraView)findViewById(R.id.myCameraView); // Initialize camera view based on ID specified in .xml file
            cameraBridgeViewBase.setVisibility(SurfaceView.VISIBLE);
            cameraBridgeViewBase.setCvCameraViewListener(this);

            // For Ryan's Calculations with Z positioning
            CameraManager manager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);
            try {
                Log.d("CAMERA DETAILS", "INSIDE CAM");
                String[] cameraIds = manager.getCameraIdList();
                for(String cameraDetails : cameraIds)
                {
                    CameraCharacteristics details = manager.getCameraCharacteristics(cameraDetails);
                    Log.d("CAMERA DETAILS", "Camera Characteristics - Facing: " + details.get(CameraCharacteristics.LENS_FACING));
                    for(float focalLength : details.get(CameraCharacteristics.LENS_INFO_AVAILABLE_FOCAL_LENGTHS))
                        Log.d("CAMERA DETAILS", "Camera Characteristics - Focal Length: " + focalLength);
                    Log.d("CAMERA DETAILS", "Camera Characteristics - Physical Size: " + details.get(CameraCharacteristics.SENSOR_INFO_PHYSICAL_SIZE));
                }
            } catch (CameraAccessException e) {
                Log.d("CAMERA", e.getMessage(), e);
            }

            /* Audio Adjusting */
            audio = (AudioManager) getSystemService(Context.AUDIO_SERVICE);
            currentVolume = audio.getStreamVolume(AudioManager.STREAM_MUSIC);
            maxVolume = audio.getStreamMaxVolume(AudioManager.STREAM_MUSIC);
            percentageOfMaxVolume = 0.1f;

            baseLoaderCallback = new BaseLoaderCallback(this) {
                @Override
                public void onManagerConnected(int status) {
                    switch(status)
                    {
                        case BaseLoaderCallback.SUCCESS:
                            cameraBridgeViewBase.enableView();
                            break;
                        default:
                            super.onManagerConnected(status); // Send the load status of OpenCV to OpenCV library manager
                            break;
                    }
                }
            };


            /* Bluetooth */
//            bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
//            if(bluetoothAdapter != null)
//            {
//                Toast.makeText(getApplicationContext(), "Bluetooth initialized.", Toast.LENGTH_LONG).show();
//                if(!bluetoothAdapter.isEnabled()){
//                    makeDiscoverable();
//                    Intent enableBluetooth = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
//                    startActivityForResult(enableBluetooth, 1);
//                    IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
//                    registerReceiver(receiver, filter);
//                    Log.d("Bluetooth Search", "Starting Bluetooth Search...");
//                    bluetoothAdapter.startDiscovery();
//
//                    /*********/
//                    //makeConnection("81:D1:26:30:BF:91"); // BTDEVICE CONNECT BY NAME
//                    /*********/
//                }
//            }
//            else
//            {
//                Toast.makeText(getApplicationContext(), "Bluetooth not supported on this device.", Toast.LENGTH_LONG).show();
//            }


            // Image Viewing
            //imageView = (ImageView)findViewById(R.id.imageView);
        }
        else {
            Toast.makeText(getApplicationContext(),"OpenCV FAILED to load", Toast.LENGTH_LONG).show();
        }
    }

    /* Bluetooth */

//    private final BroadcastReceiver receiver = new BroadcastReceiver() {
//        @Override
//        public void onReceive(Context context, Intent intent) {
//            String action = intent.getAction();
//            if(BluetoothDevice.ACTION_FOUND.equals(action)){
//                // Device has been found, get information
//                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
//                discoveredDevices.add(device);
////                String deviceName = device.getName();
////                String deviceMAC = device.getAddress();
//            }
//        }
//    };
//
//    private void makeDiscoverable() {
//        Intent discoverable = new Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE);
//        discoverable.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, 300);
//        startActivity(discoverable);
//        Log.d("DISCOVERABLE","Initiated Discoverable Request");
//    }
//
//    private void makeConnection(String MAC)
//    {
//        Log.d("BLUETOOTH CONNECTION" , "Entered Connection Function");
//        BluetoothDevice targetDevice = null;
//        try{
//            for(BluetoothDevice device : bluetoothAdapter.getBondedDevices())
//            {
//                Log.d("BLUETOOTH CONNECTION" , "Devices are populated");
//                UUID portID = UUID.randomUUID();
//                //Toast.makeText(getApplicationContext(), "UUID: " + portID.toString(), Toast.LENGTH_LONG).show();
//                if(device.getAddress().equals(MAC)) {
//                    targetDevice = device;
//                    socket = targetDevice.createRfcommSocketToServiceRecord(portID);
//                    socket.connect();
//                    Log.d("CONNECTION GOOD", "Bluetooth connection established with " + MAC);
//                    return;
//                }
//            }
//            Log.d("CONNECTION NOT FOUND", "No device name: " + MAC);
//        } catch (IOException e) {
//            Log.d("ERROR IN BLUETOOTH CONN", MAC + " could not be connected " + e.toString());
//        }
//    }

    /* Access Photos */

    public void openGallery(View v)
    {
        Intent openGalleryApp = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        startActivityForResult(openGalleryApp, 100);
    }

    public void openMusic(View v)
    {
        // I am assuming the user is running SDK 15 or higher
        Intent openMusicApp = Intent.makeMainSelectorActivity(Intent.ACTION_MAIN, Intent.CATEGORY_APP_MUSIC);
        openMusicApp.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivityForResult(openMusicApp, 100);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(requestCode == 100 && resultCode == RESULT_OK && data != null)
        {
            imageUri = data.getData();

            try {
                imageBitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), imageUri);
                Toast.makeText(getApplicationContext(), "Image Loaded", Toast.LENGTH_SHORT).show();
            } catch(IOException e) {
                e.printStackTrace();
                Toast.makeText(getApplicationContext(), "Failed load image from Android Photo Media", Toast.LENGTH_LONG).show();
            }

            imageView.setImageBitmap(imageBitmap);
        }
    }

    public void convertToGrayscale(View v)
    {
        Mat rgba = new Mat();
        Mat grayMat = new Mat();

        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inDither = false;
        options.inSampleSize = 4;

        int width = imageBitmap.getWidth();
        int height = imageBitmap.getHeight();

        grayBitmap = Bitmap.createBitmap(width, height, Bitmap.Config.RGB_565);

        // Bitmap to Mat

        Utils.bitmapToMat(imageBitmap, rgba);

        // Make the image gray

        Imgproc.cvtColor(rgba, grayMat, Imgproc.COLOR_RGB2GRAY);
        Utils.matToBitmap(grayMat, grayBitmap);

        imageView.setImageBitmap(grayBitmap);
    }

//    parseImage(Mat frame) {
//
//    }
//
//    Mat spatialToAuditory (Mat frame, QRObjects, Point personMid) {
//
//    }

    // Needed for OpenCV Camera implements :

    // Called second after camera start
    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {

        System.gc();
        frameCount++;
        frame.release();
        frame = inputFrame.rgba(); // Grab the current frames RGBA pixels

        // Take the image data from mat1 and flip is 90 degrees
        Core.transpose(frame,mat2); // Copy the mat1
        Imgproc.resize(mat2, mat3, mat3.size(), 0, 0, 0); // Resize it to fit into mat3
        Core.flip(mat3, frame, 1); // Flip map3's canvas 90 degrees, then store back onto mat1's canvas

//        // Saving mat to external storage
//          if(frameCount % nFrames == 0) {
//            if (count % 39 + nFrames == 0) {
//
//                /* INCREMENTALLY CHANGE THE VOLUME EVERY nFrames */
//                if (percentageOfMaxVolume < 1.0f) {
//                    percentageOfMaxVolume += 0.05f; // Every nFrames, increase volume by 5%
//                    currentVolume = (int) (maxVolume * percentageOfMaxVolume); // Calculate new volume
//                    audio.setStreamVolume(AudioManager.STREAM_MUSIC, currentVolume, AudioManager.FLAG_PLAY_SOUND |
//                            AudioManager.FLAG_SHOW_UI |
//                            AudioManager.FLAG_VIBRATE |
//                            AudioManager.FLAG_ALLOW_RINGER_MODES);
//                } /* !VOLUME CHANGE */
//
//                /* DEBUG */
////                Log.d("BLUETOOTH DEVICES", "DISCOVERED DEVICES:");
////                for (BluetoothDevice device : discoveredDevices){
////                    Log.d("DEVICE NAME", device.getName());
////                    Log.d("DEVICE MAC", device.getAddress());
////                }
////
////                Log.d("ADAPTER DEVICES", "BOUND DEVICES");
////                for (BluetoothDevice device : bluetoothAdapter.getBondedDevices()) {
////                    Log.d("DEVICE NAME", device.getName());
////                    Log.d("DEVICE MAC", device.getAddress());
////                }
//                /* !DEBUG */
//
//                Log.d("IMAGE STORAGE WRITE", "Image write successful");
//            }
//            else
//                Log.d("IMAGE STORAGE WRITE", "Image write failed");

            // OpenCV Image Processing
            //frame = mat1;
            Mat personMat = new Mat();
            frame.copyTo(personMat);
            //Imgproc.resize(mat1, mat1, new Size(500, 500));
            Imgproc.cvtColor(frame.clone(), personMat, Imgproc.COLOR_BGR2GRAY);
            Imgproc.GaussianBlur(personMat, personMat, new Size(21, 21), 0);

            if(first)
            {
                Log.d("SENDING", "SENDING mat1 LINE 370");
                personMat.copyTo(previousFrame);
                first = false;
                return frame;
            }

            Mat frameDifference = new Mat();
            Core.absdiff(previousFrame, personMat, frameDifference);
            Mat personThreshold = new Mat();
            Imgproc.threshold(frameDifference, personThreshold, 10, 255, Imgproc.THRESH_BINARY); // changing this could increase image quality and recognition
            Imgproc.dilate(personThreshold, personThreshold, new Mat(), new Point(), 2); // THIS MIGHT THROW

            List<MatOfPoint> personContours = new ArrayList<>();
            Imgproc.findContours(personThreshold.clone(), personContours, new Mat(), Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);

            previousFrame.release();
            personMat.copyTo(previousFrame);
            if(personContours.size() == 0) {
                Log.d("PERSON CONTOURS", "Person contours are empty");
                Log.d("SENDING", "SENDING mat1 LINE 385");
                personMat.release();
                frameDifference.release();
                return frame;
            }

            int maxWidth = 0;
            int maxHeight = 0;
            int personX = 0;
            int personY = 0;
            int avgMidX = 0;
            int avgMidY = 0;

            Rect maxRect = new Rect(0,0,0,0);

            for(MatOfPoint contour : personContours)
            {
              if(Imgproc.contourArea(contour) < mainContourSize)
                continue;

              Rect personRect = Imgproc.boundingRect(contour);
              if (personRect.width * personRect.height > maxRect.width * maxRect.height)
                maxRect = personRect;
              avgMidX += personRect.x + personRect.width/2;
              avgMidY += personRect.y + personRect.height/2;
              Imgproc.rectangle(frame, new Point(personRect.x, personRect.y), new Point(personRect.x + personRect.width, personRect.y + personRect.height), new Scalar(0, 255, 0), 2);
            }

            double focalLength = 4.67;
            double avgPersonHeight = 350;
            double sensorHeight = 7.81;
            double distanceFromCamera = 0;
            double maxDistance = 1000;
            if (maxRect.height * sensorHeight > 0)
                distanceFromCamera = (focalLength * avgPersonHeight * frame.height()) / (maxRect.height * sensorHeight);
                System.out.println("************* Distance From Camera (mm): " + String.valueOf(distanceFromCamera));

            if (distanceFromCamera > 0 && frameCount % 4 == 0) {
                double volume = Math.abs(distanceFromCamera - maxDistance) / maxDistance <= 1 ? Math.abs(distanceFromCamera - maxDistance) / maxDistance : 1;
                System.out.println("------------------------------- Volume Level: " + String.valueOf(volume));
                    audio.setStreamVolume(AudioManager.STREAM_MUSIC, (int)(volume * maxVolume), AudioManager.FLAG_PLAY_SOUND |
                            AudioManager.FLAG_SHOW_UI |
                            AudioManager.FLAG_VIBRATE |
                            AudioManager.FLAG_ALLOW_RINGER_MODES);

                    /* !VOLUME CHANGE */

                    System.gc();
            }
            avgMidX /= personContours.size();
            avgMidY /= personContours.size();

//            QRobjects = parseImageForQR(frame);
//
//            frame = spatialToAuditory(frame, QRObjects, new Point(avgMidX, avgMidY));

            Log.d("SENDING", "SENDING FRAME LINE 416");
            // Imgproc.cvtColor(frame, frame, Imgproc.COLOR_GRAY2BGR);
            personMat.release();
            frameDifference.release();
            return frame;
//        }
//        Imgproc.cvtColor(frame, frame, Imgproc.COLOR_GRAY2BGR);
//        return frame; // Return upright Camera view
    }

    // Saves Mat to external storage, returns boolean for successful write or fail to do so
    private Boolean writeMatToExternalStorage(Mat inputFrameMat)
    {
        File externalImageStoragePath = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);

        String matFilename = frameCount + "_OPENCV" + ".jpg";

        File matFile = new File(externalImageStoragePath, matFilename);
        String matFilePath = matFile.toString();
        Log.d("WRITE MAT TO STORAGE @", matFilePath);
        return Imgcodecs.imwrite(matFilePath,inputFrameMat);
    }

    private Boolean writeMatToExternalStorage(Mat inputFrameMat, String ID)
    {
        File externalImageStoragePath = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);

        String matFilename = frameCount + "_OPENCV" +  "_" + ID + ".jpg";

        File matFile = new File(externalImageStoragePath, matFilename);
        String matFilePath = matFile.toString();
        Log.d("WRITE MAT TO STORAGE @", matFilePath);
        return Imgcodecs.imwrite(matFilePath,inputFrameMat);
    }

    @Override
    public void onCameraViewStopped() {
        // Deallocate resources used for camera mats when the camera is not in use
        mat1.release();
        mat2.release();
        mat3.release();
        frame.release();
        previousFrame.release();

        // Bluetooth
        // unregisterReceiver(receiver);
    }

    // Called first on camera start
    @Override
    public void onCameraViewStarted(int width, int height) {
        mat1 = new Mat(width, height, CvType.CV_8UC4); // Multidimensional array that stores image data
        mat2 = new Mat(width, height, CvType.CV_8UC4);
        mat3 = new Mat(width, height, CvType.CV_8UC4);
        frame = new Mat(width, height, CvType.CV_8UC4);
        previousFrame = new Mat(width, height, CvType.CV_8UC4);
    }

    @Override
    protected void onPause() {
        super.onPause();
        if(cameraBridgeViewBase != null)
        {
            cameraBridgeViewBase.disableView();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();

        if(!OpenCVLoader.initDebug())
        {
            Toast.makeText(getApplicationContext(), "OpenCV Error in Resume", Toast.LENGTH_LONG).show();
        }
        else
        {
            Toast.makeText(getApplicationContext(), "OpenCV Resumed", Toast.LENGTH_SHORT).show();

            setVolumeControlStream(AudioManager.STREAM_MUSIC); // Bind volume to music when app relaunches
            percentageOfMaxVolume = 0.05f; // Every nFrames, increase volume by 5%
            currentVolume = (int) (maxVolume * percentageOfMaxVolume); // Calculate new volume
            audio.setStreamVolume(AudioManager.STREAM_MUSIC, currentVolume, AudioManager.FLAG_PLAY_SOUND|
                    AudioManager.FLAG_SHOW_UI |
                    AudioManager.FLAG_VIBRATE |
                    AudioManager.FLAG_ALLOW_RINGER_MODES);

            baseLoaderCallback.onManagerConnected(BaseLoaderCallback.SUCCESS);
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        if(cameraBridgeViewBase != null)
        {
            cameraBridgeViewBase.disableView();
        }

        // BLUETOOTH
//        try {
//            socket.close();
//        } catch (IOException e) {
//            Log.d("ERROR IN BT CLOSE", "BT socket could not be connected " + e.toString());
//        }
    }
}
