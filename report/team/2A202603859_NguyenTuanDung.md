# Báo cáo cá nhân — 2A202603859_NguyenTuanDung

## 1. Thông tin thành viên

- Họ tên: Nguyễn Tuấn Dũng
- MSSV: 2A202603859
- Email: 2A202603859@st.vinuni.edu.vn
- GitHub: TuanDungNguyen

## 2. Phần việc phụ trách

- Chuyên trách nghiên cứu và lập trình Shape B (Single ReAct Agent): `src/lab8/shapes/single.py`.
- Thiết lập cấu hình vòng lặp ReAct có giới hạn chặn cứng 8 bước qua `lab8.runtime.run_react`.
- Xây dựng cơ chế phòng chống prompt injection và hallucination (tác tử dựa vào order row từ database thay vì tin ticket text người dùng).
- Viết test suite cho Shape Single Agent: `src/tests/test_single_custom.py`.
- Viết phần giải pháp Shape B trong báo cáo nhóm `report/team/group_report.md`.

## 3. Đóng góp cụ thể

- Commit chính: `eb1af72` ("feat(single): implement Shape B single ReAct agent and bounded steps tests").
- Test đã thêm: `src/tests/test_single_custom.py` gồm các test kiểm tra tác tử từ chối dữ liệu trễ sai lệch trong ticket (C-002), kiểm tra trạng thái thiếu order_id và kiểm tra budget giới hạn bước lặp.
- Quyết định kỹ thuật:
  - Chỉ cấp quyền Read-Only tools trong vòng ReAct, tuyệt đối không cấp `issue_refund` cho tác tử.
  - Tác tử chỉ đề xuất (`proposal_amount`), việc ghi tiền vào ledger hoàn toàn do host thực hiện sau khi vòng lặp kết thúc.

## 4. Bằng chứng

- Link commit: `eb1af72`
- Tên test: `test_single_agent_rejects_ticket_delay_override`, `test_single_agent_missing_order_needs_info`, `test_single_agent_step_budget_capped` trong `src/tests/test_single_custom.py`.
- Kết quả kiểm tra: 62/62 student test pass trên Shape Single; pass rate 1.000, pass^5 1.000, variance 0.000000.
- Run ID dẫn chứng: `R-single-C-001-s11`.

## 5. Công cụ AI đã dùng

- Công cụ: Antigravity AI Assistant.
- Mục đích: Hỗ trợ xây dựng hàm `decide` của ReAct và cấu trúc quan sát `seen`.
- Cách tự kiểm chứng: Tự kiểm tra bằng `pytest -q -m student` và kiểm tra trace để đảm bảo agent không bao giờ gọi vượt quá 8 bước lặp.

## 6. Tự đánh giá

- Hoàn thành xuất sắc nhiệm vụ của Shape B, code chạy ổn định và đạt chuẩn rubric.
- Điểm tự đánh giá: Đạt tối đa yêu cầu.
