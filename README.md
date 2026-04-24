# Dashboard Xác Thực

## 1) Mô tả

Dashboard vận hành xác thực theo tỉnh, sinh từ:
- `f_total.xlsx` (chỉ tiêu/KPI theo tỉnh)
- file xác thực dạng pipe-delimited `xac_thuc_...txt`

Pipeline chính: `luong_du_lieu.py`.

Đầu ra chính:
- `f_total_cap_nhat.xlsx`
- `data.json` (được `report.html` đọc để render giao diện)

## 2) Tính năng hiện tại

- Topbar ngày báo cáo lấy động theo `report_date` trong `data.json`.
- Filter tỉnh global dùng chung cho dashboard (trừ tab Xu hướng).
- Khi chọn `Tất cả tỉnh`:
	- Bảng T1/T2 giữ rule cũ: nhóm tỉnh đạt KH + top 10 thấp nhất.
- Khi chọn 1 tỉnh bất kỳ:
	- T1/T2 luôn hiển thị 1 dòng của tỉnh đó.
	- KPI thẻ trái cập nhật theo tỉnh (bao gồm cả CMT9 và Yếu thế).
	- Tab `Tỉnh` dùng cùng filter global (đã bỏ dropdown riêng trong panel này).
- Tab `Xu hướng` giữ logic riêng, không bị tác động bởi filter global.

## 3) Cấu trúc dữ liệu JSON quan trọng

`data.json` gồm các phần chính:
- `summary.total_card`
- `summary.offline_card`
- `summary.by_province` (KPI đầy đủ theo từng tỉnh)
- `t1.dat_kh`, `t1.thap_nhat`, `t1.all_rows`
- `t2.dat_kh`, `t2.thap_nhat`, `t2.all_rows`
- `trend.labels`, `trend.provinces`, `trend.all_provinces`, `trend.national`

## 4) Yêu cầu môi trường

- Python 3.8+
- Packages: `pandas`, `openpyxl`

## 5) Cài môi trường

### Bash

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### PowerShell (Windows)

```powershell
python -m venv .venv
\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 6) Chạy pipeline

### Cách 1: script bash

```bash
bash run_pipeline.sh
```

### Cách 2: chạy trực tiếp

```powershell
\.venv\Scripts\python.exe luong_du_lieu.py
```

Có thể truyền thêm tham số:

```powershell
\.venv\Scripts\python.exe luong_du_lieu.py --from-date 2026-04-19 --report-date 2026-04-23
```

## 7) Chạy local dashboard

```powershell
\.venv\Scripts\python.exe server.py
```

Sau đó mở URL được in ra màn hình:
- ưu tiên `http://localhost:8000/report.html`
- nếu cổng 8000 bận, server tự fallback sang `8001`

## 8) Publish GitHub Pages

- Branch publish: `main`
- `index.html` redirect về `report.html`
- URL public:
	- `https://nguyenhuuhoang3697.github.io/dashboard_xacthuc_thongtin/`

Nếu chưa thấy bản mới:
1. Chờ 1-2 phút để Pages build xong.
2. Hard refresh trình duyệt (`Ctrl+F5`).

## 9) File chính

- `luong_du_lieu.py`: pipeline tính toán và xuất JSON.
- `report.html`: giao diện dashboard.
- `server.py`: static server UTF-8 cho local.
- `data.json`: dữ liệu đầu ra để render dashboard.
- `run_pipeline.sh`: script chạy pipeline nhanh.