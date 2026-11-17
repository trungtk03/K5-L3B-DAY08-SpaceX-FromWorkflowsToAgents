# Báo cáo cá nhân — 2A202603748_LuongThiHongHanh

## 1. Thông tin thành viên

- Họ tên: Lương Thị Hồng Hạnh
- MSSV: 2A202603748
- Email: 2A202603748@st.vinuni.edu.vn
- GitHub: hanhlth

## 2. Phần việc phụ trách

- Chuyên trách độ bền dữ liệu (Durability), Ledger Idempotency và kiểm thử Crash Safety.
- Chạy và nghiệm thu bộ Crash test suite (`src/reports/crash.json`) đạt yêu cầu 20/20.
- Thực thi toàn bộ bộ Benchmark suite 4 shape × 5 seed (`src/reports/benchmark.json`).
- Hoàn thiện tài liệu quyết định kiến trúc `report/team/decision_adr.md` và phiếu nghiên cứu `report/team/research_card.md` (chủ đề R2 và thực nghiệm ablation).
- Viết test suite cho Durability & Crash: `src/tests/test_durability_custom.py`.
- Viết Mục 4 (Kết quả thực nghiệm) và Mục 7 (Hạn chế) trong báo cáo nhóm `report/team/group_report.md`.

## 3. Đóng góp cụ thể

- Commit chính: `b5125b5` ("feat(durability): add durability & crash tests, run crash suite 20/20 and benchmark").
- Test đã thêm: `src/tests/test_durability_custom.py` gồm các test kiểm tra crash injection tại các điểm nhạy cảm, resume không ghi đúp ledger và tính idempotent của nhiều lần gọi lại cùng claim.
- Quyết định kỹ thuật:
  - Khẳng định và chứng minh rằng `workflow` là shape tối ưu nhất theo nguyên tắc "ít tự chủ nhất mà làm được việc", nhờ phương sai bằng 0 và chi phí thấp hơn 72% so với swarm.
  - Thiết kế bài thực nghiệm ablation làm rõ nguyên nhân Swarm thất bại ở seed 55 do thiếu cơ chế kiểm chứng dữ liệu độc lập từ DB.

## 4. Bằng chứng

- Link commit: `b5125b5`
- Tên test: `test_durability_crash_and_recovery_single_ledger_row`, `test_idempotency_second_call_keeps_original_state` trong `src/tests/test_durability_custom.py`.
- Bằng chứng báo cáo: `src/reports/crash.json` đạt `crash_safety: "20/20"`, `src/reports/benchmark.json` đầy đủ 4 shape × 14 claim × 5 seed.
- Run ID dẫn chứng: `R-workflow-C-001-s11`.

## 5. Công cụ AI đã dùng

- Công cụ: Antigravity AI Assistant.
- Mục đích: Hỗ trợ phân tích dữ liệu benchmark và lập bảng đối chiếu các chỉ số pass rate, pass^5, seed variance và cost per success.
- Cách tự kiểm chứng: Tự chạy lại các lệnh benchmark và crash_test để đối soát số liệu khớp 100% với file JSON nộp bài.

## 6. Tự đánh giá

- Hoàn thành trọn vẹn toàn bộ các báo cáo định lượng và kiểm thử độ bền hệ thống.
- Điểm tự đánh giá: Đạt tối đa yêu cầu.
