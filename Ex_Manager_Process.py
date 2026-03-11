# chứa các hàm xử lý dữ liệu

from datetime import datetime
import json

class Ex_Manager_Process:

    ds = []

    # --- Nhập dữ liệu, thao tác với transaction ---
    def add_transaction(self, tr_type, tr_category, tr_amount, date_str, tr_note):

        try:
            tr_amount = int(tr_amount)

            if tr_amount <= 0:
                return False, "Số tiền phải là số dương!"

            # kiểm tra định dạng ngày
            
            transaction = {
                "date": date_str,
                "type": tr_type,
                "category": tr_category,
                "amount": tr_amount,
                "note": tr_note
            }

            Ex_Manager_Process.ds.append(transaction)

            return True, "Transaction added successfully"

        except ValueError:
            return False, "Số tiền không hợp lệ!"

    @classmethod
    def get_transactions(cls):
        return cls.ds

    @classmethod
    def reset_transactions(cls):
        cls.ds = []


    # --- Xử lý dữ liệu từ list transactions ---
    @classmethod
    def tinh_tong(cls):     # Tính tổng của tất các type và category
        totals = {
            "Income": {"total": 0, "Salary": 0, "Allowance": 0, "Full-time job": 0, "Part-time job": 0, "Other": 0},
            "Expense": {"total": 0, "Food": 0, "Transport": 0, "Entertainment": 0, "Education": 0, "Other": 0},
            "Saving": {"total": 0}
        }

        for trans in cls.ds:
            tr_type = trans["type"]
            tr_category = trans["category"]
            tr_amount = trans["amount"]

            if trans["type"] in totals:
                totals[tr_type]["total"] += tr_amount
                if trans["category"] in totals[tr_type]:
                    totals[tr_type][tr_category] += tr_amount
        totals['Saving']['total'] = totals['Income']['total'] - totals['Expense']['total']
        return totals

    @classmethod
    def lay_thang_tu_transactions(cls):
        if not cls.ds:
            return None # tránh việc ds rỗng gây crash
        
        month = cls.ds[0]["date"].strip()
        d, m, y = month.split("/")
        month = f"{m}/{y}"
        return month


    # --- làm việc với JSON (đọc trước - ghi sau) ---
    @staticmethod
    def lay_du_lieu_tu_json():
        try:
            with open("data.json", "r", encoding="utf8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"Safety Box": 0, "Months": {}}

        return data
    
    @classmethod
    def kiem_tra_thang_tu_json(cls, month):
        data = cls.lay_du_lieu_tu_json()
        for m in data["Months"]:
            if month == m:
                return True 


    # --- Lưu dữ liệu vào JSON   
    @classmethod
    def luu_vao_json(cls, month):
        data = cls.lay_du_lieu_tu_json()
        month_data = cls.tinh_tong()

        # Lưu tháng
        data["Months"][month] = month_data

        # Cập nhật safety box
        sb_truoc = data["Safety Box"]
        saving = month_data["Saving"]["total"]
        data["Safety Box"] = sb_truoc + saving

        with open("data.json", "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False, indent=3)
    # --- Chức năng Compare ---   
    @classmethod
    def compare_month(cls):
        """So sánh dữ liệu từ 2 tháng gần nhất"""
        data = cls.lay_du_lieu_tu_json()
        months = list(data["Months"].keys())
        if len(months) < 2:
            return {
                "status": False,
                "message": "Không đủ dữ liệu để so sánh (cần ít nhất 2 tháng)",
                "comparison": None
            }
        
        # Sắp xếp theo tháng và lấy 2 tháng gần nhất
        months.sort()
        last_month = months[-2]
        this_month = months[-1]
        
        # Lấy dữ liệu từ hai tháng
        last_data = data["Months"][last_month]
        this_data = data["Months"][this_month]
        
        # Hàm lấy tổng
        def get_total(d, key):
            return d.get(key, {}).get("total", 0)
        
        # So sánh 3 loại: Income, Saving, Expense
        sections = ["Income", "Expense", "Saving"]
        comparison = {}
        
        for section in sections:
            last_value = get_total(last_data, section)
            this_value = get_total(this_data, section)
            
            # Tính phần trăm thay đổi
            if last_value == 0:
                if this_value == 0:
                    percent_change = 0
                else:
                    percent_change = 100  # Tăng từ 0
            else:
                percent_change = ((this_value - last_value) / last_value) * 100
            
            # Xác định tăng hay giảm
            change_type = "Tăng" if percent_change >= 0 else "Giảm"
            
            comparison[section] = {
                "last_month": last_month,
                "last_value": last_value,
                "this_month": this_month,
                "this_value": this_value,
                "percent_change": percent_change,
                "change_type": change_type,
                "change_value": this_value - last_value
            }
        
        return {
            "status": True,
            "message": f"So sánh giữa tháng {last_month} và {this_month}",
            "comparison": comparison
        }

# if __name__ == "__main__":
#     ex = Ex_Manager_Process()

#     ex.add_transaction("Income", "Salary", 1000, "07/03/2026", "Lương tháng")
#     ex.add_transaction("Income", "Allowance", 200, "07/03/2026", "Trợ cấp")
#     ex.add_transaction("Expense", "Food", 50, "07/03/2026", "Ăn trưa")
#     ex.add_transaction("Expense", "Transport", 20, "07/03/2026", "Xe bus")
#     ex.add_transaction("Saving", "Emergency", 100, "07/03/2026", "Tiết kiệm")
#     ex.add_transaction("Saving", "Goal", 200, "09/02/2026", "Tiết kiệm")
#     ex.add_transaction("Saving", "Goal", 1000, "09/02/2026", "Tiết kiệm")
#     ex.add_transaction("Income", "Salary", 1000, "07/03/2026", "Lương tháng")
#     ex.add_transaction("Income", "Allowance", 200, "07/03/2026", "Trợ cấp")
#     ex.add_transaction("Expense", "Food", 50, "07/03/2026", "Ăn trưa")
#     ex.add_transaction("Expense", "Transport", 20, "07/03/2026", "Xe bus")
#     ex.add_transaction("Saving", "Emergency", 100, "07/03/2026", "Tiết kiệm")
#     ex.add_transaction("Saving", "Goal", 200, "09/02/2026", "Tiết kiệm")
#     ex.add_transaction("Saving", "Goal", 1000, "09/02/2026", "Tiết kiệm")

# totals = Ex_Manager_Process.tinh_tong()
# print(totals)
# x = Ex_Manager_Process.lay_thang_tu_transactions()
# print(x)
# # # print(Ex_Manager_Process.ds)
# i = ex.lay_thang_tu_json("1/102")
# print(i)