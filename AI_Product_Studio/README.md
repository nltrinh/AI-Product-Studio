# 📸 AI Product Studio - Sinh ảnh sản phẩm phong cách Studio

**Sinh viên:** [Tên Của Bạn] - [Mã SV]
**GVHD:** TS. Lê Quang Hùng

## 📌 Giới thiệu
Hệ thống tự động thay đổi phông nền sản phẩm (Product Background Generation) giữ nguyên cấu trúc sản phẩm và tạo bối cảnh studio chuyên nghiệp sử dụng **Stable Diffusion + ControlNet + LoRA**.

## 📂 Cấu trúc Repository
- `dataset/`: Bộ dữ liệu 40 ảnh chất lượng cao dùng để train LoRA.
- `notebooks/`: Mã nguồn thực nghiệm (Train, Inference, Eval).
- `results/`: Kết quả hình ảnh và đánh giá độ đo.

## 🚀 Cách chạy Demo (Google Colab)
Bạn có thể chạy ngay ứng dụng bằng cách nhấn vào nút dưới đây:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](LINK_ĐẾN_FILE_2_APP_DEMO_CỦA_BẠN_TRÊN_GITHUB)

*Lưu ý: Cần tải file trọng số LoRA và sửa đường dẫn trong code.*

## 📊 Kết quả
- **CLIP Score trung bình:** 35.90
- **Đánh giá:** Hình ảnh giữ nguyên cấu trúc sản phẩm, ánh sáng tự nhiên.