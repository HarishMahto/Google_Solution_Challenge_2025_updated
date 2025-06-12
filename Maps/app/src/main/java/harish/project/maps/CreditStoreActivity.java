package harish.project.maps;

import android.os.Bundle;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;

public class CreditStoreActivity extends AppCompatActivity {

    private TextView creditPointsText;
    private RecyclerView voucherRecyclerView;
    private VoucherAdapter voucherAdapter;

    private int userCreditPoints = 50; // Example, should be loaded from persistent storage
    private List<Voucher> availableVouchers = new ArrayList<>();
    private List<Voucher> claimedVouchers = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_credit_store);

        creditPointsText = findViewById(R.id.creditPoints);
        voucherRecyclerView = findViewById(R.id.voucherRecyclerView);

        // Sample vouchers
        availableVouchers.add(new Voucher("Train ticket discount", "Get a discount on your next train ticket.", 1000, "Available"));
        availableVouchers.add(new Voucher("Toll Discount", "Save on your next toll payment.", 700, "Available"));

        voucherAdapter = new VoucherAdapter(availableVouchers, userCreditPoints, new VoucherAdapter.OnClaimListener() {
            @Override
            public void onClaim(Voucher voucher) {
                userCreditPoints -= voucher.getRequiredPoints();
                creditPointsText.setText(String.valueOf(userCreditPoints));
                voucher.setStatus("Active");
                claimedVouchers.add(voucher);
                availableVouchers.remove(voucher);
                voucherAdapter.setUserCreditPoints(userCreditPoints);
                voucherAdapter.notifyDataSetChanged();
                // Optionally, persist claimedVouchers and userCreditPoints
            }
        });

        voucherRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        voucherRecyclerView.setAdapter(voucherAdapter);

        creditPointsText.setText(String.valueOf(userCreditPoints));
    }
}