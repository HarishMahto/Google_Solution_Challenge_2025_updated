package harish.project.maps;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class VoucherAdapter extends RecyclerView.Adapter<VoucherAdapter.VoucherViewHolder> {
    public interface OnClaimListener {
        void onClaim(Voucher voucher);
    }

    private List<Voucher> vouchers;
    private int userCreditPoints;
    private OnClaimListener claimListener;

    public VoucherAdapter(List<Voucher> vouchers, int userCreditPoints, OnClaimListener claimListener) {
        this.vouchers = vouchers;
        this.userCreditPoints = userCreditPoints;
        this.claimListener = claimListener;
    }

    public void setUserCreditPoints(int points) {
        this.userCreditPoints = points;
    }

    @NonNull
    @Override
    public VoucherViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_voucher, parent, false);
        return new VoucherViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull VoucherViewHolder holder, int position) {
        Voucher voucher = vouchers.get(position);
        holder.title.setText(voucher.getTitle());
        holder.description.setText(voucher.getDescription());
        //holder.points.setText(voucher.getRequiredPoints() + " coins");
        holder.points.setText(String.valueOf(voucher.getRequiredPoints()));
        holder.claimButton.setEnabled(userCreditPoints >= voucher.getRequiredPoints());
        holder.claimButton.setAlpha(userCreditPoints >= voucher.getRequiredPoints() ? 1f : 0.5f);

        holder.claimButton.setOnClickListener(v -> {
            if (claimListener != null && userCreditPoints >= voucher.getRequiredPoints()) {
                claimListener.onClaim(voucher);
            }
        });
    }

    @Override
    public int getItemCount() {
        return vouchers.size();
    }

    static class VoucherViewHolder extends RecyclerView.ViewHolder {
        TextView title, description, points;
        Button claimButton;

        public VoucherViewHolder(@NonNull View itemView) {
            super(itemView);
            title = itemView.findViewById(R.id.voucherTitle);
            description = itemView.findViewById(R.id.voucherDescription);
            points = itemView.findViewById(R.id.voucherPoints);
            claimButton = itemView.findViewById(R.id.claimButton);
        }
    }
}