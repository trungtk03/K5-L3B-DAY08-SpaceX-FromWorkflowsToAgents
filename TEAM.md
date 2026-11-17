# Team

## Thông tin nhóm

- Tên nhóm: SpaceX
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY08-SpaceX-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/trungtk03/K5-L3B-DAY08-SpaceX-FromWorkflowsToAgents, main, b1aef5f

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Hoàng Trung | 2A202603826 | 2A202603826@st.vinuni.edu.vn | trungtk03 | Workflow + Integration (Lead) |
|   2 | Nguyễn Tuấn Dũng | 2A202603859 | 26ai.dungnt16@vinuni.edu.vn | DungNguyen74 | Single ReAct Agent |
|   3 | Phùng Thị Nhài | 2A202603725 | 2A202603725@st.vinuni.edu.vn | nhaipt | Orchestrator + Handoff Security |
|   4 | Lương Thị Hồng Hạnh | 2A202603748 | 2A202603748@st.vinuni.edu.vn | hanhlth | Durability, Benchmark & Evaluation |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Nguyễn Hoàng Trung | Workflow + Integration | 1c75422 | tests/test_workflow_custom.py |
| Nguyễn Tuấn Dũng | Single ReAct Agent | eb1af72 | tests/test_single_custom.py |
| Phùng Thị Nhài | Orchestrator + Handoff | b65a5ad | tests/test_orchestrator_custom.py |
| Lương Thị Hồng Hạnh | Durability + Evaluation | b5125b5 | tests/test_durability_custom.py |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## 2A202603826_NguyenHoangTrung

### Phần việc phụ trách

- Trưởng nhóm (Lead), quản lý repo, hiện thực Shape A (Workflow).

### Đóng góp cụ thể

- Commit `1c75422`, viết `src/lab8/shapes/workflow.py`, thêm test `src/tests/test_workflow_custom.py`.

### Bằng chứng

- Pass rate 1.000, 62/62 student test pass, run id `R-workflow-C-001-s11`.

## 2A202603859_NguyenTuanDung

### Phần việc phụ trách

- Shape B (Single ReAct Agent), cấu hình chặn cứng 8 steps, thiết lập worker mode chỉ đọc, phòng chống prompt injection & hallucination.

### Đóng góp cụ thể

- Commit `eb1af72` và commit cập nhật, viết `src/lab8/shapes/single.py`, thêm bộ test suite `src/tests/test_single_custom.py` (7 tests).

### Bằng chứng

- Pass rate 1.000, 62/62 student test pass, 7/7 custom test pass, run id `R-single-C-001-s11`.

## 2A202603725_PhungThiNhai

### Phần việc phụ trách

- Shape C (Orchestrator + Investigators), khử khuẩn Handoff, an toàn bảo mật ranh giới.

### Đóng góp cụ thể

- Commit `b65a5ad`, viết `src/lab8/shapes/orchestrator.py`, thêm test `src/tests/test_orchestrator_custom.py`.

### Bằng chứng

- Pass rate 1.000, 62/62 student test pass, secret leak = 0, approval bypass = 0, run id `R-orchestrator-C-001-s11`.

## 2A202603748_LuongThiHongHanh

### Phần việc phụ trách

- Durability, Ledger Idempotency, Crash Test Suite, Benchmark 4 shapes × 5 seeds, ADR & Research card.

### Đóng góp cụ thể

- Commit `b5125b5`, chạy crash suite 20/20, chạy benchmark, thêm test `src/tests/test_durability_custom.py`.

### Bằng chứng

- `crash_safety = 20/20` (`reports/crash.json`), benchmark 4 shape x 14 claim x 5 seed (`reports/benchmark.json`), ADR và Research card hoàn chỉnh.
