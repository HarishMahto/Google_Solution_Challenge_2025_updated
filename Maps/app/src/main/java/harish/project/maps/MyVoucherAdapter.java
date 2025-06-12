package harish.project.maps;

import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;


import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class MyVoucherAdapter extends RecyclerView.Adapter<MyVoucherAdapter.MyVoucherViewHolder> {
    private List<Voucher> vouchers;

    public MyVoucherAdapter(List<Voucher> vouchers) {
        this.vouchers = vouchers;
    }

    @NonNull
    @Override
    public MyVoucherViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_my_voucher, parent, false);
        return new MyVoucherViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull MyVoucherViewHolder holder, int position) {
        Voucher voucher = vouchers.get(position);
        holder.title.setText(voucher.getTitle());
        holder.description.setText(voucher.getDescription());
        holder.status.setText(voucher.getStatus());
        // Optionally, set color based on status
        if ("Active".equals(voucher.getStatus())) {
            holder.status.setTextColor(Color.parseColor("#4CAF50"));
        } else if ("Used".equals(voucher.getStatus())) {
            holder.status.setTextColor(Color.parseColor("#888"));
        } else if ("Expired".equals(voucher.getStatus())) {
            holder.status.setTextColor(Color.parseColor("#F44336"));
        }
    }

    @Override
    public int getItemCount() {
        return vouchers.size();
    }

    static class MyVoucherViewHolder extends RecyclerView.ViewHolder {
        TextView title, description, status;

        public MyVoucherViewHolder(@NonNull View itemView) {
            super(itemView);
            title = itemView.findViewById(R.id.voucherTitle);
            description = itemView.findViewById(R.id.voucherDescription);
            status = itemView.findViewById(R.id.voucherStatus);
        }
    }
}