# chứa các hàm xử lý dữ liệu

from datetime import datetime
import json

class Ex_Manager_Process:

    ds = []

    def add_transaction(self, tr_type, tr_category, tr_amount, tr_date, tr_note):

        try:
            tr_amount = float(tr_amount)

            if tr_amount <= 0:
                return False, "Số tiền phải là số dương!"

            # kiểm tra định dạng ngày
            
            transaction = {
                "date": tr_date,
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
    def tinh_tong(cls):     # Tính tổng của tất các type và category
        totals = {
            "Income": {"total": 0, "Salary": 0, "Allowance": 0, "Part-time job": 0, "Full-time job": 0, "Other": 0},
            "Expense": {"total": 0, "Food": 0, "Transport": 0, "Entertainment": 0, "Education": 0, "Other": 0},
            "Saving": {"total": 0}
        }

        for trans in cls.ds:
            tr_type = trans["type"]
            tr_amount = trans["amount"]
            tr_category = trans["category"]

            if trans["type"] in totals:
                totals[tr_type]["total"] += tr_amount
                if trans["category"] in totals[tr_type]:
                    totals[tr_type][tr_category] += tr_amount

            totals['Saving']['total'] = totals['Income']['total'] - totals['Expense']['total']
        
        return totals

    #Lưu trữ có 2 phần: safety box và các tháng
    @classmethod
    def luu_thang(cls, month):
        data = cls.lay_du_lieu_tu_json()
        month_data = cls.tinh_tong()
        data["Months"][month] = month_data

        with open("data.json", "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=None, indent= 3)

    @classmethod
    def luu_safety_box(cls):

        data = cls.lay_du_lieu_tu_json()

        sb_truoc = data["Safety Box"]
        month_data = cls.tinh_tong()
        saving = month_data["Saving"]["total"]

        sb_moi = sb_truoc + saving
        data["Safety Box"] = sb_moi

        with open("data.json", "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False, indent=3)
        
    @staticmethod
    def lay_du_lieu_tu_json():
        try:
            with open("data.json", "r", encoding="utf8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"Safety Box": 0, "Months": {}}

        return data
    
    @classmethod
    def reset_transactions(cls):
        cls.ds = []

    @classmethod
    def lay_thang_tu_transactions(cls):
        data = cls.ds
        month = data[0]["date"].strip()
        
        d, m, y = month.split("/")
        month = f"{m}/{y}"
        return month
    
    @classmethod
    def kiem_tra_thang_tu_json(cls, month):
        data = cls.lay_du_lieu_tu_json()
        for m in data["Months"]:
            if month == m:
                return True        

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
        sections = ["Income", "Saving", "Expense"]
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
    
    @classmethod
    def get_comparison_summary(cls):
        """Trả về tóm tắt kết quả so sánh dạng text"""
        result = cls.compare_month()
        
        if not result["status"]:
            return result["message"]
        
        comp = result["comparison"]
        summary = f"\n{'='*60}\n"
        summary += f"So sánh: Tháng {comp['Income']['last_month']} vs Tháng {comp['Income']['this_month']}\n"
        summary += f"{'='*60}\n\n"
        
        for section, data in comp.items():
            summary += f"{section}:\n"
            summary += f"  Tháng trước: {data['last_value']:,.2f}\n"
            summary += f"  Tháng này:  {data['this_value']:,.2f}\n"
            summary += f"  Thay đổi:   {data['change_value']:+,.2f}\n"
            summary += f"  {data['change_type']}: {abs(data['percent_change']):.2f}%\n\n"
        
        summary += f"{'='*60}\n"
        return summary

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