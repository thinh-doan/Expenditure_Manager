# danh sách chi tiêu, thêm, xoá, tính tổng tiền, lưu file
from datetime import datetime, timedelta

class Ex_Manager_Process:
    ds = []
    
    def add_transaction(self, tr_type, tr_category, tr_amount, tr_date, tr_note):
        try:
            tr_amount = float(tr_amount)
            if tr_amount <= 0:
                return False, "Số tiền phải là số dương!"
            
            try: # why try not if?
                # Validate date format
                datetime.strptime(tr_date, "%d/%m/%Y")
            except ValueError:
                return False, "Định dạng ngày không hợp lệ, nhập lại DD/MM/YYYY!"

            transaction = {
                'date': tr_date,
                'type': tr_type,
                'category': tr_category,
                'amount': tr_amount,
                'note': tr_note
            }
            Ex_Manager_Process.ds.append(transaction)
            return True, "Transaction added successfully"
        
        except ValueError:
            return False, "Invalid amount"

    @classmethod    
    def get_transactions(cls):
        return cls.ds

    def luu_tru(self):
        pass

    def hien_thi(self):
        pass




         