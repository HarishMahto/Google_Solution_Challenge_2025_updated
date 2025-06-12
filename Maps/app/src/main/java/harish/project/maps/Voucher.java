package harish.project.maps;

public class Voucher {
    private String title;
    private String description;
    private int requiredPoints;
    private String status; // "Available", "Active", "Used", "Expired"

    public Voucher(String title, String description, int requiredPoints, String status) {
        this.title = title;
        this.description = description;
        this.requiredPoints = requiredPoints;
        this.status = status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public int getRequiredPoints() {
        return requiredPoints;
    }

    public String getStatus() {
        return status;
    }
}