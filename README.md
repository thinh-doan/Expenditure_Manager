# PHẦN MỀM QUẢN LÝ CHI TIÊU CÁ NHÂN (EXPENDITURE MANAGER)
# Mục tiêu hệ thống: 
Giúp người dùng quản lý tài chính thông minh hơn. Nhu cầu phổ thông nhưng lại rất thực tế để tiến hành xây dựng phần mềm
# Nền tảng xây dựng: 
- Ngôn ngữ lập trình Python
- Thiết kế giao diện QT Designer
- Thư viện hỗ trợ đọc giao diện: PyQt6 
- Lưu trữ dữ liệu bằng file JSON 
# Các chức năng chính :
# 1. Thêm Thu nhập (Add Income)
   - Category (cố định) : Salary (lương), Allowance (phụ cấp), Full-time job, Part_time job, Other (Khác)
   - Amount : nhập lượng tiền, không cố định đơn vị tiền tệ
   - Date: chọn ngày xảy ra giao dịch (người dùng chọn từ lịch thay vì nhập thủ công)
   - Note : nơi ghi chú
# 2. Thêm Chi tiêu (Add Expense)
   - Category (cố định) : Food (Thực phẩm), Transport (Đi lại), Entertainment (Giải trí), Education (Giáo dục), Other (Khác)
   - Amount : nhập lượng tiền, không cố định đơn vị tiền tệ
   - Date: chọn ngày xảy ra giao dịch (người dùng chọn từ lịch thay vì nhập thủ công)
   - Note : nơi ghi chú
# 3. Tính tổng kết (Summarize)
   - Tính năng Safety Box (két sắt) : bản chất là số dư tài khoản tích lũy của người dùng, có hỗ trợ tùy chỉnh số dư lúc đầu
     
       --> Safety Box = Safety Box (tháng trước) + Saving (tháng này)
   - Tính tổng Income
   - Tính tổng Expense
   - Tính tổng Saving (tiết kiệm) = Tổng Income - Tổng Expense
# 4. So sánh tổng 2 tháng gần nhất (Compare)
   Lấy dữ liệu là Tổng của Income, Expense, Saving tháng trước so sánh với Tổng của Income, Expense, Saving tháng này
   
   Cho thấy sự thay đổi về lượng tiền và tăng giảm tỷ lệ %
# 5. Tìm kiếm dữ liệu giao dịch của 1 tháng bất kỳ 
  Các giao dịch được ghi nhận theo tháng và được lưu vào file lưu trữ dữ liệu data.json
  
  Vì vậy kể cả khi có tắt phần mềm đi thì dữ liệu vẫn không hề bị mất đi. Và đây cũng chính là tiền đề để thực hiện chức năng tìm kiếm giao dịch theo tháng, bằng cách truy xuất trực tiếp từ file data.json
# Giao diện người dùng
Xem trực tiếp tại folder ui 
# Cấu trúc các file code 
1. File Ex_Manager_Ext

  Thực hiện các chức năng liên quan trực tiếp đến giao diện như liên kết nút, hiển thị bảng ...

2. File Ex_Manager_Process
  
  Thực hiện các ràng buộc logic, công thức tính toán, lưu trữ JSON ...

3. File giao diện Python
  
  Được generate trực tiếp từ 3 file ui trong folder ui, là "bản vẽ chi tiết" của phần mềm gồm:
   - Inter_Expense.py
   - Inter_Income.py
   - Inter_MainWindow.py

   
