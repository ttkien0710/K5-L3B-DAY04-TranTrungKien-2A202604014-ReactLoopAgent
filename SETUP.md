# CP1 — Setup và khám phá tools

## Mốc Git

- Repo cá nhân: `ttkien0710/K5-L3B-DAY04-TranTrungKien-2A202604014-ReactLoopAgent`.
- Ngày 11/11/2026: bổ sung mốc setup đã bỏ sót trước khi tiếp tục các checkpoint sau.
- Tại commit này, `agent.py` giữ nguyên bản đề từ `origin/main` (dfdc975).
- Code CP2–CP3 đã viết trước đó được giữ ở bản sao local để khôi phục sau khi push mốc này. Đây là mốc bổ sung, không phải lịch sử thực hiện được dựng lại.

## Kiểm tra thực tế

- Python 3.14.6; project dùng standard library, không cần cài package ngoài.
- Đã chạy hai lệnh khám phá tools trong GUIDE.md ngày 11/11/2026.
- `get_status('github', 'Actions')` trả JSON: component Actions là `operational`, có 5 incident trả về và 23 incident khớp trong 50 incident gần nhất.
- `get_incident_details('cloudflare', 'wp49bp8bqo6c')` trả `ok: true`, incident FedRAMP, 2 updates và URL nguồn.
- Đây là snapshot ngày 09/11/2026, không phải trạng thái live.

## Điều cần hiểu

- `get_status` tìm theo chuỗi trong 50 incident gần nhất, trả tối đa 5 incident; kết quả rỗng không chứng minh incident không tồn tại.
- `get_incident_details` trả chi tiết, URL và các updates có giới hạn; cần đọc `truncated` và `updates_total`.
- Incident Cloudflare mẫu ảnh hưởng khách hàng FedRAMP, không suy rộng cho toàn bộ khách hàng.

## Cấu hình API còn cần xác nhận

- Eval hiện có dùng provider `gemini`, model và judge `gemini-3.5-flash-lite`, max steps 8.
- Phiên thực hiện mốc này chưa có biến `GEMINI_API_KEY`, `PROVIDER` hoặc `MODEL`.
- Chưa xác nhận lại API hoạt động trong phiên này; chưa đánh dấu toàn bộ CP1 hoàn tất.
- Đặt các biến môi trường trong terminal chạy bài; không commit hoặc chia sẻ API key. Chương trình không tự đọc `.env`.
- Sau khi push mốc setup, tiếp tục CP2–CP3 với code đã giữ lại. CP4 cần eval đủ 22 case và điểm tổng khác `null` trước khi phân tích cải tiến.
## Xác nhận bổ sung ngày 12/11/2026

- Đã gọi Gemini thật bằng model `gemini-3.5-flash-lite`; key giữ trong `.env` bị Git ignore.
- CP2–CP3 được kiểm chứng qua trace thật của baseline và unit tests.
- CP4: `eval_before.json` được chấm đủ 22/22 case, điểm tổng 95.45/100.
- Runner bổ sung: `scripts/run_reliable_evals.py`, chạy runner chính thức với timeout 180 giây, tối đa 2 retry khi gặp lỗi truyền tải tạm thời. Dùng cùng chính sách cho before/after.
- Code baseline vẫn được giữ local trong `agent copy.py`; bản nộp sử dụng `agent.py`.
