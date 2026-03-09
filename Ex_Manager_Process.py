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
            'Income': {'total': 0, 'Salary': 0, 'Allowance': 0, 'Part-time job': 0, 'Full-time job': 0, 'Other': 0},
            'Saving': {'total': 0, 'Emergency': 0, 'Goal': 0, 'General': 0, 'Other': 0},
            'Expense': {'total': 0, 'Food': 0, 'Transport': 0, 'Entertainment': 0, 'Education': 0, 'Other': 0}
        }

        for trans in cls.ds:
            tr_type = trans['type']
            tr_amount = trans['amount']
            tr_category = trans['category']

            if trans['type'] in totals:
                totals[tr_type]['total'] += tr_amount
                if trans['category'] in totals[tr_type]:
                    totals[tr_type][tr_category] += tr_amount

        return totals

    #Lưu trữ có 2 phần: safety box và các tháng
    @classmethod
    def luu_thang(cls, month):
        # try:
        #     with open('data.json', 'r', encoding='utf8') as f:
        #         data = json.load(f)
        # except:
        #     data = {'Safety Box': 0, 'Months': {}}

        # month_data = cls.tinh_tong()
        # data['Months'][month] = month_data

        # with open('data.json', 'w', encoding='utf8') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=3)
        data = cls.lay_du_lieu_tu_json()
        month_data = cls.tinh_tong()
        data['Months'][month]
        with open('data.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=3)
        

    @classmethod
    def luu_safety_box(cls):
        # try:
        #     with open('data.json', 'r', encoding='utf8') as f:
        #         data = json.load(f)
        # except:
        #     data = {'Safety Box': 0, 'Months': {}}

        # sb_amount = data['Safety Box']

        # month_data = cls.tinh_tong()    
        # sb_thang_nay = month_data['Income']['total'] - month_data['Expense']['total']
        # sb_amount += sb_thang_nay
        
        # data['Safety Box'] = sb_amount

        # with open('data.json', 'w', encoding='utf8') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=3)
        data = cls.lay_du_lieu_tu_json()
        sb_truoc = data["safety Box"]
        month_data = cls.tinh_tong()
        income = month_data['Income']['total']
        expense = month_data['Expense']['total']
        sb_moi = sb_truoc + income - expense
        data['Safety Box'] = sb_moi       
        

    @staticmethod
    def lay_du_lieu_tu_json():
        try:
            with open('data.json', 'r', encoding='utf8') as f:
                    data = json.load(f)
        except:
            data = {'Safety Box': 0, 'Months': {}}
        return data
    
    @classmethod
    def reset_transactions(cls):
        cls.ds = []

# if __name__ == "__main__":
#     ex = Ex_Manager_Process()

#     ex.add_transaction("Income", "Salary", 1000, "07/03/2026", "Lương tháng")
#     ex.add_transaction("Income", "Allowance", 200, "07/03/2026", "Trợ cấp")
#     ex.add_transaction("Expense", "Food", 50, "07/03/2026", "Ăn trưa")
#     ex.add_transaction("Expense", "Transport", 20, "07/03/2026", "Xe bus")
#     ex.add_transaction("Saving", "Emergency", 100, "07/03/2026", "Tiết kiệm")
#     ex.add_transaction("Saving", "Goal", 200, "09/02/2026", "Tiết kiệm")
#     ex.add_transaction("Saving", "Goal", 1000, "09/02/2026", "Tiết kiệm")

#     totals = Ex_Manager_Process.tinh_tong()

# print(totals)
Ex_Manager_Process.luu_safety_box()

# month = "2026-4"
# Ex_Manager_Process.luu_thang(month)
