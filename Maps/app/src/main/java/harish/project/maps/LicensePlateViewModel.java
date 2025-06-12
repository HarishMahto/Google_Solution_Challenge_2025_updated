package harish.project.maps;

import android.app.Application;
import android.net.Uri;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;

import com.google.mlkit.vision.common.InputImage;
import com.google.mlkit.vision.text.Text;
import com.google.mlkit.vision.text.TextRecognition;
import com.google.mlkit.vision.text.TextRecognizer;
import com.google.mlkit.vision.text.latin.TextRecognizerOptions;

import java.io.IOException;

public class LicensePlateViewModel extends AndroidViewModel {
    private LicensePlateRepository repository;
    private MutableLiveData<String> recognizedText = new MutableLiveData<>();
    private MutableLiveData<Uri> capturedImageUri = new MutableLiveData<>();
    private TextRecognizer textRecognizer;

    public LicensePlateViewModel(@NonNull Application application) {
        super(application);
        repository = new LicensePlateRepository();
        textRecognizer = TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS);
    }

    public LiveData<String> getRecognizedText() {
        return recognizedText;
    }

    public LiveData<Uri> getCapturedImageUri() {
        return capturedImageUri;
    }

    public LiveData<String> getUploadStatus() {
        return repository.getUploadStatus();
    }

    public void setCapturedImageUri(Uri uri) {
        capturedImageUri.setValue(uri);
    }

    public void processImage(Uri imageUri) {
        try {
            InputImage image = InputImage.fromFilePath(getApplication().getApplicationContext(), imageUri);
            textRecognizer.process(image)
                    .addOnSuccessListener(this::extractLicensePlate)
                    .addOnFailureListener(e -> {
                        recognizedText.setValue("Error: " + e.getMessage());
                    });
        } catch (IOException e) {
            recognizedText.setValue("Error: " + e.getMessage());
        }
    }

    private void extractLicensePlate(Text text) {
        String extractedText = "";
        for (Text.TextBlock block : text.getTextBlocks()) {
            for (Text.Line line : block.getLines()) {
                String lineText = line.getText();
                // Simple filtering for license plate format (can be improved)
                if (lineText.matches(".*[A-Z0-9]{5,}.*")) {
                    extractedText = lineText.replaceAll("\\s+", "");
                    break;
                }
            }
            if (!extractedText.isEmpty()) break;
        }

        if (extractedText.isEmpty()) {
            recognizedText.setValue("No license plate detected");
        } else {
            recognizedText.setValue(extractedText);
        }
    }

    public void saveLicensePlate() {
        Uri imageUri = capturedImageUri.getValue();
        String plateText = recognizedText.getValue();
        
        if (imageUri != null && plateText != null && !plateText.startsWith("Error") && !plateText.equals("No license plate detected")) {
            repository.saveLicensePlate(imageUri, plateText);
        } else {
            repository.getUploadStatus().setValue("Error: Invalid image or text");
        }
    }

    @Override
    protected void onCleared() {
        super.onCleared();
        textRecognizer.close();
    }
}