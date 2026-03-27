# PHẦN MỀM QUẢN LÝ CHI TIÊU CÁ NHÂN (EXPENDITURE MANAGER)
## Mục tiêu của phần mềm
Theo dõi các khoản thu nhập và chi tiêu hàng tháng.

Lưu trữ các danh mục chi tiêu cụ thể trong từng tháng và tổng số tiền tiết kiệm một cách chặt chẽ.

Giúp người dùng quản lý tài chính cá nhân, có cái nhìn tổng quan và đánh giá kết quả chi tiêu của bản thân.  
## Công nghệ sử dụng
- Python - ngôn ngữ lập trình chính
- QtDesigner - Thiết kế giao diện
- PyQt6 - kết nối Python và giao diện Qt
- QStylesheet - Trang trí giao diện
- JSON - Lưu trữ dữ liệu
## Cấu trúc project    
<img width="429" height="198" alt="image" src="https://github.com/user-attachments/assets/3febfe20-1da0-4988-8901-fd7c0d6f1993" />

## Các chức năng chính  
### 1. Thêm Thu nhập (Add Income)
   - Category (cố định) : Salary (lương), Allowance (phụ cấp), Full-time job, Part_time job, Other (Khác)
   - Amount : nhập lượng tiền, không cố định đơn vị tiền tệ
   - Date: chọn ngày xảy ra giao dịch (người dùng chọn từ lịch thay vì nhập thủ công)
   - Note : nơi ghi chú
### 2. Thêm Chi tiêu (Add Expense)
   - Category (cố định) : Food (Thực phẩm), Transport (Đi lại), Entertainment (Giải trí), Education (Giáo dục), Other (Khác)
   - Amount : nhập lượng tiền, không cố định đơn vị tiền tệ
   - Date: chọn ngày xảy ra giao dịch (người dùng chọn từ lịch thay vì nhập thủ công)
   - Note : nơi ghi chú
### 3. Tính tổng kết (Summarize)
   - Tính năng Safety Box (két sắt) : bản chất là số dư tài khoản tích lũy của người dùng, có hỗ trợ tùy chỉnh số dư lúc đầu
     
       --> Safety Box = Safety Box (tháng trước) + Saving (tháng này)
   - Tính tổng Income
   - Tính tổng Expense
   - Tính tổng Saving (tiết kiệm) = Tổng Income - Tổng Expense
### 4. So sánh tổng 2 tháng gần nhất (Compare)
   Lấy dữ liệu là Tổng của Income, Expense, Saving tháng trước so sánh với Tổng của Income, Expense, Saving tháng này
   
   Cho thấy sự thay đổi về lượng tiền và tăng giảm tỷ lệ %
### 5. Tìm kiếm dữ liệu giao dịch của 1 tháng bất kỳ 
  Các giao dịch được ghi nhận theo tháng và được lưu vào file lưu trữ dữ liệu data.json
  
  Vì vậy kể cả khi có tắt phần mềm đi thì dữ liệu vẫn không hề bị mất đi. Và đây cũng chính là tiền đề để thực hiện chức năng tìm kiếm giao dịch theo tháng, bằng cách truy xuất trực tiếp từ file data.json
  
## Một số hạn chế của phần mềm
Phần mềm này là đồ án đầu tiên của mình, với kinh nghiệm và thời gian còn hạn chế nên phần mềm không thể tránh khỏi sự thiếu sót và chưa tối ưu.

Hạn chế của phần mềm:
- Số lượng danh mục (Categories) bị giới hạn, người dùng thêm giao dịch (transaction) từ một danh mục không có sẵn chỉ có thể chọn "Other categories".
- Không thể thêm giao dịch mới vào các tháng cũ sau khi đã bấm REFRESH, nếu cố ý thêm một giao dịch mới với DATE chứa tháng cũ thì toàn bộ dữ liệu trong tháng cũ đó sẽ mất và được ghi lại từ đầu.
- Không lưu lại giao dịch vào tệp tin lưu trữ json, chỉ lưu tổng số tiền của các danh mục.

## Người đóng góp
- Duy Thịnh (Me) - code chính
- Mai Hương - tham gia code, tối ưu xử lý
- Như Quỳnh - góp ý, sửa logic chức năng SUMMARIZE
- Huyền Trang - hỗ trợ trang trí giao diện
- Duy Trọng - sửa giao diện
