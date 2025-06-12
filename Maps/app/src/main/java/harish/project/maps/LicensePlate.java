package harish.project.maps;

import java.util.Date;

public class LicensePlate {
    private String id;
    private String plateNumber;
    private Date timestamp;
    private String imageUrl;

    // Empty constructor needed for Firestore
    public LicensePlate() {
    }

    public LicensePlate(String plateNumber, Date timestamp, String imageUrl) {
        this.plateNumber = plateNumber;
        this.timestamp = timestamp;
        this.imageUrl = imageUrl;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getPlateNumber() {
        return plateNumber;
    }

    public void setPlateNumber(String plateNumber) {
        this.plateNumber = plateNumber;
    }

    public Date getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }
}