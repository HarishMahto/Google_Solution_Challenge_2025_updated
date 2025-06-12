package harish.project.maps;

import android.net.Uri;

import androidx.lifecycle.MutableLiveData;

import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

import java.util.Date;
import java.util.UUID;

public class LicensePlateRepository {
    private FirebaseFirestore db;
    private FirebaseStorage storage;
    private MutableLiveData<String> uploadStatus = new MutableLiveData<>();

    public LicensePlateRepository() {
        db = FirebaseFirestore.getInstance();
        storage = FirebaseStorage.getInstance();
    }

    public MutableLiveData<String> getUploadStatus() {
        return uploadStatus;
    }

    public void saveLicensePlate(Uri imageUri, String plateNumber) {
        uploadStatus.setValue("Uploading image...");
        
        // Generate a unique filename
        String filename = "license_plates/" + UUID.randomUUID().toString() + ".jpg";
        StorageReference storageRef = storage.getReference().child(filename);
        
        // Upload image to Firebase Storage
        UploadTask uploadTask = storageRef.putFile(imageUri);
        uploadTask.addOnSuccessListener(taskSnapshot -> {
            // Get the download URL
            storageRef.getDownloadUrl().addOnSuccessListener(uri -> {
                String imageUrl = uri.toString();
                
                // Create license plate object
                LicensePlate licensePlate = new LicensePlate(plateNumber, new Date(), imageUrl);
                
                // Save to Firestore
                db.collection("license_plates")
                        .add(licensePlate)
                        .addOnSuccessListener(documentReference -> {
                            uploadStatus.setValue("Success");
                        })
                        .addOnFailureListener(e -> {
                            uploadStatus.setValue("Error saving data: " + e.getMessage());
                        });
            });
        }).addOnFailureListener(e -> {
            uploadStatus.setValue("Error uploading image: " + e.getMessage());
        }).addOnProgressListener(snapshot -> {
            double progress = (100.0 * snapshot.getBytesTransferred()) / snapshot.getTotalByteCount();
            uploadStatus.setValue("Uploading: " + (int) progress + "%");
        });
    }
}