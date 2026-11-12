# Mini App Nhóm C – Vận động thể chất và thói quen ngồi

## 1. Nội dung
Mini App hỗ trợ học sinh phân tích dữ liệu khảo sát ẩn danh về:
- Phút vận động vừa–mạnh/ngày
- Số ngày vận động/tuần
- Hoạt động thể chất thường tham gia
- Thời gian ngồi liên tục tối đa (phút/lần)

Ứng dụng có 3 phần: Tự kiểm tra thói quen; Phân tích khảo sát; Kiến thức & an toàn.

## 2. Chạy trên máy tính
Cài Python 3.10 trở lên, mở Terminal/CMD tại thư mục dự án và chạy:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Cài thư viện và chạy:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 3. Cấu trúc dữ liệu
Nếu dùng Excel, ứng dụng đọc sheet `Du_lieu_khao_sat` và bỏ qua 2 dòng đầu (`skiprows=2`).
Nếu dùng CSV, hàng đầu tiên phải là tên cột.

Tên 5 cột bắt buộc:
1. Mã HS
2. Phút vận động vừa-mạnh/ngày
3. Số ngày vận động/tuần
4. Hoạt động thể chất thường tham gia
5. Thời gian ngồi liên tục tối đa (phút/lần)

Có thể dùng tệp CSV mẫu trong thư mục `data`.

## 4. Triển khai miễn phí bằng GitHub và Streamlit Community Cloud
1. Giải nén ZIP.
2. Tạo repository GitHub mới và tải toàn bộ nội dung thư mục dự án lên repository.
3. Truy cập https://share.streamlit.io/ và đăng nhập bằng GitHub.
4. Chọn **Create app**, chọn repository, branch và file chính `app.py`.
5. Chọn **Deploy**. Chờ Streamlit cài thư viện trong `requirements.txt`.
6. Mở đường dẫn ứng dụng được cấp để kiểm tra.

Không tải dữ liệu khảo sát có thông tin định danh lên repository công khai. Nên dùng dữ liệu đã ẩn danh hoặc dữ liệu mô phỏng.

## 5. Vai trò của AI
AI có thể hỗ trợ học sinh gợi ý giao diện, tạo bản nháp mã nguồn, giải thích hàm và tìm lỗi. Nhóm phải kiểm tra, chạy thử và hiểu các phần chính. Ứng dụng không tích hợp API AI trả phí và không cần khóa API để vận hành.

## 6. Quy ước và giới hạn
- Mốc 60 phút vận động/ngày là mốc tham khảo giáo dục cho lứa tuổi học sinh.
- Ngồi liên tục trên 60 phút là quy ước nhắc nghỉ giải lao của dự án, không phải ngưỡng y tế.
- Dữ liệu tự khai báo có thể sai số. Kết quả chỉ phục vụ học tập, truyền thông sức khỏe học đường; không dùng để chẩn đoán.
