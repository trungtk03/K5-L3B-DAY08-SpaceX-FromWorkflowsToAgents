# Báo cáo cá nhân — 2A202603725_PhungThiNhai

## 1. Thông tin thành viên

- Họ tên: Phùng Thị Nhài
- MSSV: 2A202603725
- Email: 2A202603725@st.vinuni.edu.vn
- GitHub: nhaipt

## 2. Phần việc phụ trách

- Chuyên trách nghiên cứu và lập trình Shape C (Orchestrator + Read-only Investigators): `src/lab8/shapes/orchestrator.py`.
- Bảo mật ranh giới hệ thống: Xây dựng cơ chế khử khuẩn dữ liệu bàn giao (`lab8.handoff.make_handoff` và `sanitize`).
- Đảm bảo rà soát không rò rỉ secret (`CANARY_SECRET_*`) và thông tin định danh cá nhân (PII) qua trace.
- Viết test suite bảo mật: `src/tests/test_orchestrator_custom.py`.
- Viết phần bảo mật ranh giới và sanitization trong báo cáo nhóm `report/team/group_report.md`.

## 3. Đóng góp cụ thể

- Commit chính: `b65a5ad` ("feat(orchestrator): implement Shape C orchestrator, handoff sanitization and security tests").
- Test đã thêm: `src/tests/test_orchestrator_custom.py` gồm các test kiểm tra trace không chứa token hay PII, và kiểm tra tính toán bồi thường hư hại đúng điều kiện.
- Quyết định kỹ thuật:
  - Chỉ cho phép investigator sử dụng các công cụ trong allowlist chỉ đọc (`lookup_order`, `lookup_policy`, `compute_compensation`).
  - Gói handoff bóc tách sạch sẽ `parent_secret` và `raw_headers_json` trước khi chuyển giao.

## 4. Bằng chứng

- Link commit: `b65a5ad`
- Tên test: `test_orchestrator_sanitizes_handoff_and_no_leak`, `test_orchestrator_resolves_valid_damage_claim` trong `src/tests/test_orchestrator_custom.py`.
- Kết quả kiểm tra: 62/62 student test pass trên Shape Orchestrator; pass rate 1.000, pass^5 1.000, variance 0.000000; số lượng secret leak = 0 và approval bypass = 0.
- Run ID dẫn chứng: `R-orchestrator-C-001-s11`.

## 5. Công cụ AI đã dùng

- Công cụ: Antigravity AI Assistant.
- Mục đích: Hỗ trợ cấu hình tích hợp giữa orchestrator và runner điều tra viên chỉ đọc.
- Cách tự kiểm chứng: Tự kiểm tra các file trace JSON sinh ra trong `traces/` bằng công cụ quét chuỗi cấm để chắc chắn không có rò rỉ.

## 6. Tự đánh giá

- Hoàn thành đầy đủ các tiêu chuẩn bảo mật khắt khe nhất của bài toán.
- Điểm tự đánh giá: Đạt tối đa yêu cầu.
