package harish.project.maps;

import android.Manifest;
import android.content.ContentValues;
 import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.core.CameraSelector;
import androidx.camera.core.ImageCapture;
import androidx.camera.core.ImageCaptureException;
import androidx.camera.core.Preview;
import androidx.camera.lifecycle.ProcessCameraProvider;
import androidx.camera.view.PreviewView;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.lifecycle.ViewModelProvider;

import com.bumptech.glide.Glide;
import com.google.common.util.concurrent.ListenableFuture;

import java.text.SimpleDateFormat;
import java.util.Locale;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class LicensePlateActivity extends AppCompatActivity {
    private static final int REQUEST_CODE_PERMISSIONS = 10;
    private static final String[] REQUIRED_PERMISSIONS = new String[]{
            Manifest.permission.CAMERA,
            Manifest.permission.WRITE_EXTERNAL_STORAGE
    };

    private PreviewView viewFinder;
    private ImageView capturedImageView;
    private Button captureButton;
    private Button saveButton;
    private TextView plateNumberTextView;
    private TextView statusTextView;

    private ImageCapture imageCapture;
    private ExecutorService cameraExecutor;
    private LicensePlateViewModel viewModel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_license_plate);

        // Initialize views
        viewFinder = findViewById(R.id.viewFinder);
        capturedImageView = findViewById(R.id.capturedImageView);
        captureButton = findViewById(R.id.captureButton);
        saveButton = findViewById(R.id.saveButton);
        plateNumberTextView = findViewById(R.id.plateNumberTextView);
        statusTextView = findViewById(R.id.statusTextView);

        // Initialize ViewModel
        viewModel = new ViewModelProvider(this).get(LicensePlateViewModel.class);

        // Set up observers
        viewModel.getRecognizedText().observe(this, text -> {
            plateNumberTextView.setText(text);
            saveButton.setEnabled(!text.startsWith("Error") && !text.equals("No license plate detected"));
        });

        viewModel.getCapturedImageUri().observe(this, uri -> {
            if (uri != null) {
                viewFinder.setVisibility(android.view.View.GONE);
                capturedImageView.setVisibility(android.view.View.VISIBLE);
                Glide.with(this).load(uri).into(capturedImageView);
                viewModel.processImage(uri);
            } else {
                viewFinder.setVisibility(android.view.View.VISIBLE);
                capturedImageView.setVisibility(android.view.View.GONE);
            }
        });

        viewModel.getUploadStatus().observe(this, status -> {
            statusTextView.setText(status);
            if (status.equals("Success")) {
                Toast.makeText(this, "License plate saved successfully", Toast.LENGTH_SHORT).show();
                // Reset UI for next capture
                viewModel.setCapturedImageUri(null);
                plateNumberTextView.setText("Plate Number Will Appear Here");
                saveButton.setEnabled(false);
                statusTextView.setText("Ready to capture");
            } else if (status.startsWith("Error")) {
                Toast.makeText(this, status, Toast.LENGTH_LONG).show();
            }
        });

        // Set up button click listeners
        captureButton.setOnClickListener(v -> {
            if (viewFinder.getVisibility() == android.view.View.VISIBLE) {
                takePhoto();
            } else {
                // Reset to camera view
                viewModel.setCapturedImageUri(null);
            }
        });

        saveButton.setOnClickListener(v -> viewModel.saveLicensePlate());

        // Request camera permissions
        if (allPermissionsGranted()) {
            startCamera();
        } else {
            ActivityCompat.requestPermissions(this, REQUIRED_PERMISSIONS, REQUEST_CODE_PERMISSIONS);
        }

        cameraExecutor = Executors.newSingleThreadExecutor();
    }

    private void takePhoto() {
        if (imageCapture == null) return;

        // Create timestamped output file
        String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(System.currentTimeMillis());
        ContentValues contentValues = new ContentValues();
        contentValues.put(MediaStore.MediaColumns.DISPLAY_NAME, "IMG_" + timestamp);
        contentValues.put(MediaStore.MediaColumns.MIME_TYPE, "image/jpeg");

        // Create output options object
        ImageCapture.OutputFileOptions outputOptions = new ImageCapture.OutputFileOptions.Builder(
                getContentResolver(),
                MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
                contentValues)
                .build();

        // Capture the image
        imageCapture.takePicture(
                outputOptions,
                ContextCompat.getMainExecutor(this),
                new ImageCapture.OnImageSavedCallback() {
                    @Override
                    public void onImageSaved(@NonNull ImageCapture.OutputFileResults outputFileResults) {
                        Uri savedUri = outputFileResults.getSavedUri();
                        if (savedUri != null) {
                            viewModel.setCapturedImageUri(savedUri);
                            statusTextView.setText("Processing image...");
                        } else {
                            statusTextView.setText("Error: Could not save image");
                        }
                    }

                    @Override
                    public void onError(@NonNull ImageCaptureException exception) {
                        statusTextView.setText("Error: " + exception.getMessage());
                    }
                });
    }

    private void startCamera() {
        ListenableFuture<ProcessCameraProvider> cameraProviderFuture = ProcessCameraProvider.getInstance(this);

        cameraProviderFuture.addListener(() -> {
            try {
                // Camera provider is now guaranteed to be available
                ProcessCameraProvider cameraProvider = cameraProviderFuture.get();

                // Set up the preview use case
                Preview preview = new Preview.Builder().build();
                preview.setSurfaceProvider(viewFinder.getSurfaceProvider());

                // Set up the capture use case
                imageCapture = new ImageCapture.Builder()
                        .setCaptureMode(ImageCapture.CAPTURE_MODE_MINIMIZE_LATENCY)
                        .build();

                // Select back camera
                CameraSelector cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA;

                // Unbind any bound use cases before rebinding
                cameraProvider.unbindAll();

                // Bind use cases to camera
                cameraProvider.bindToLifecycle(this, cameraSelector, preview, imageCapture);

            } catch (ExecutionException | InterruptedException e) {
                // Handle any errors
                statusTextView.setText("Error starting camera: " + e.getMessage());
            }
        }, ContextCompat.getMainExecutor(this));
    }

    private boolean allPermissionsGranted() {
        for (String permission : REQUIRED_PERMISSIONS) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                return false;
            }
        }
        return true;
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQUEST_CODE_PERMISSIONS) {
            startCamera();
//            if (allPermissionsGranted()) {
//                startCamera();
//            } else {
//                Toast.makeText(this, "Permissions not granted by the user.", Toast.LENGTH_SHORT).show();
//                finish();
//            }
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        cameraExecutor.shutdown();
    }
}