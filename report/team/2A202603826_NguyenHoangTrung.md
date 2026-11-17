# Báo cáo cá nhân — 2A202603826_NguyenHoangTrung

## 1. Thông tin thành viên

- Họ tên: Nguyễn Hoàng Trung
- MSSV: 2A202603826
- Email: 26ai.trungnh@vinui.edu.vn
- GitHub: trungtk03

## 2. Phần việc phụ trách

- Trưởng nhóm (Team Lead), chịu trách nhiệm điều phối công việc, tạo fork repo và quản lý tiến độ.
- Thiết lập môi trường và kiểm tra smoke ban đầu (`python -m lab8.smoke`).
- Hiện thực Shape A (Deterministic Workflow): `src/lab8/shapes/workflow.py`.
- Viết test suite cho Shape Workflow: `src/tests/test_workflow_custom.py`.
- Quản lý `TEAM.md`, viết Mục 1, 2, 3 trong báo cáo nhóm `report/team/group_report.md`.

## 3. Đóng góp cụ thể

- Commit chính: `1c75422` ("feat(workflow): implement Shape A deterministic workflow and unit tests").
- Test đã thêm: `src/tests/test_workflow_custom.py` gồm các test case kiểm tra claim không tồn tại, đơn hàng thiếu order_id và đơn hàng ngoài phạm vi sở hữu của principal.
- Quyết định kỹ thuật:
  - Tách bạch hoàn toàn việc tính tiền (thuộc về `compute_compensation`) và không cho model quyết định số tiền.
  - Luôn truyền quote đầy đủ vào `durability.issue_refund` để host xử lý trần đơn hàng nhất quán.
  - Ghi trace chuẩn `Trace contract v1` ở mọi nhánh return, đảm bảo `check_trace` pass.

## 4. Bằng chứng

- Link commit: `1c75422`
- Tên test: `test_workflow_nonexistent_claim_fails_gracefully`, `test_workflow_missing_order_needs_info`, `test_workflow_escalates_unowned_order` trong `src/tests/test_workflow_custom.py`.
- Kết quả kiểm tra: 62/62 student test pass trên Shape Workflow; 14/14 claim pass trên cả 5 seeds với pass rate 1.000, variance 0.000000.
- Run ID dẫn chứng: `R-workflow-C-001-s11`.

## 5. Công cụ AI đã dùng

- Công cụ: Antigravity AI Assistant.
- Mục đích: Hỗ trợ rà soát các nhánh rẽ điều kiện của `workflow.py`, đối chiếu ma trận test T01–T14 với hợp đồng trace.
- Cách tự kiểm chứng: Tự chạy lệnh `python -m pytest -q -m student -o addopts= -k workflow` và `python -m lab8.check_submission` để đảm bảo 100% test xanh và 0 FAIL.

## 6. Tự đánh giá

- Hoàn thành đầy đủ và vượt tiến độ mọi nhiệm vụ được giao.
- Điểm tự đánh giá: Đạt tối đa yêu cầu.
