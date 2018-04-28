package com.example.grubs.opencvtest;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.SurfaceView;
import android.widget.ImageView;
import android.widget.Toast;
import android.view.View;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.JavaCameraView;
import org.opencv.android.OpenCVLoader;
import org.opencv.android.Utils;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import java.io.File;
import java.io.IOException;
import java.net.URI;

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
    Mat mat1, mat2, mat3;
    BaseLoaderCallback baseLoaderCallback; // Callback interface for OpenCV libraries

    /* Images */

    ImageView imageView;
    Uri imageUri;

    int count = 0;

        /* Grayscaling */
        Bitmap grayBitmap, imageBitmap;

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

            // Image Viewing
            imageView = (ImageView)findViewById(R.id.imageView);
        }
        else {
            Toast.makeText(getApplicationContext(),"OpenCV FAILED to load", Toast.LENGTH_LONG).show();
        }
    }

    /* Access Photos */

    public void openGallery(View v)
    {
        Intent myIntent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        startActivityForResult(myIntent, 100);
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

    // Needed for OpenCV Camera implements :

    // Called second after camera start
    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {

        mat1 = inputFrame.rgba(); // Grab the current frames RGBA pixels

        // Take the image data from mat1 and flip is 90 degrees
        Core.transpose(mat1,mat2); // Copy the mat1
        Imgproc.resize(mat2, mat3, mat3.size(), 0, 0, 0); // Resize it to fit into mat3
        Core.flip(mat3, mat1, 1); // Flip map3's canvas 90 degrees, then store back onto mat1's canvas

        // Saving mat to external storage
        if(count % 40 == 0) {
            if (writeMatToExternalStorage(mat1))
                Log.d("IMAGE STORAGE WRITE", "Image write successful");
            else
                Log.d("IMAGE STORAGE WRITE", "Image write successful");
        }
        count++;

        return mat1; // Return upright Camera view
    }

    // Saves Mat to external storage, returns boolean for successful write or fail to do so
    private Boolean writeMatToExternalStorage(Mat inputFrameMat)
    {
        File externalImageStoragePath = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);

        String matFilename = "OPENCV_" + count +".jpg";

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
    }

    // Called first on camera start
    @Override
    public void onCameraViewStarted(int width, int height) {
        mat1 = new Mat(width, height, CvType.CV_8UC4); // Multidimensional array that stores image data
        mat2 = new Mat(width, height, CvType.CV_8UC4);
        mat3 = new Mat(width, height, CvType.CV_8UC4);
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
    }
}
