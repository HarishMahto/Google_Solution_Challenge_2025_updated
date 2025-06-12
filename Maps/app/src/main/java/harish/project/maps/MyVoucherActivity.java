package harish.project.maps;

import android.os.Bundle;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;

public class MyVoucherActivity extends AppCompatActivity {
    private RecyclerView myVoucherRecyclerView;
    private MyVoucherAdapter myVoucherAdapter;
    private List<Voucher> claimedVouchers = new ArrayList<>(); // Should be loaded from persistent storage

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my_voucher);

        myVoucherRecyclerView = findViewById(R.id.myVoucherRecyclerView);

        // Example: Load claimed vouchers (should be passed from CreditStoreActivity or loaded from storage)
        claimedVouchers.add(new Voucher("Train ticket discount", "Get a discount on your next train ticket.", 1000, "Active"));
        claimedVouchers.add(new Voucher("Toll Discount", "Save on your next toll payment.", 700, "Active"));

        myVoucherAdapter = new MyVoucherAdapter(claimedVouchers);
        myVoucherRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        myVoucherRecyclerView.setAdapter(myVoucherAdapter);
    }
}