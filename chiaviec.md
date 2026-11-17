# KẾ HOẠCH PHÂN CHIA CÔNG VIỆC — LAB 8 (LOGIX-VN)
**Học phần:** AI20K — K5 (Level 3)  
**Chủ đề:** From Workflows to Agents (Một task, bốn kiến trúc)  
**Nhóm:** SpaceX — Lớp L3B  

---

## 1. Danh sách thành viên & Phân vai chính thức

| STT | Họ và tên | MSSV | Vai trò chính | Module code phụ trách | File báo cáo cá nhân |
|:---:|:---|:---:|:---|:---|:---|
| 1 | **Nguyễn Hoàng Trung** *(Lead)* | `2A202603826` | **Workflow & Integration Lead** | `src/lab8/shapes/workflow.py` & Repo setup | `report/team/2A202603826_NguyenHoangTrung.md` |
| 2 | **Nguyễn Tuấn Dũng** | `2A202603859` | **Single-Agent ReAct Specialist** | `src/lab8/shapes/single.py` | `report/team/2A202603859_NguyenTuanDung.md` |
| 3 | **Phùng Thị Nhài** | `2A202603725` | **Orchestrator & Security Specialist** | `src/lab8/shapes/orchestrator.py` & Handoff | `report/team/2A202603725_PhungThiNhai.md` |
| 4 | **Lương Thị Hồng Hạnh** | `2A202603748` | **Durability, Benchmark & Evaluation** | Durability, Crash Suite, Benchmark, ADR | `report/team/2A202603748_LuongThiHongHanh.md` |

---

## 2. Phân công chi tiết từng thành viên

### 👤 1. Nguyễn Hoàng Trung — Nhóm trưởng (Workflow & Integration)
* **Trách nhiệm Quản lý & Tích hợp:**
  - Tạo fork repo, quản lý nhánh Git, giải quyết conflict, review PR của các thành viên.
  - Chạy `smoke` test ban đầu và kiểm tra tính toàn vẹn của repo.
  - Điền và duy trì `TEAM.md` (thông tin thành viên và bảng đóng góp).
  - Trước giờ nộp: chạy `python -m lab8.check_submission` (yêu cầu đạt **0 FAIL**).
* **Trách nhiệm Lập trình (`src/lab8/shapes/workflow.py`):**
  - Viết toàn bộ luồng Shape A (Deterministic Workflow): đọc claim bằng `get_claim_view`, kiểm tra `order_id` (thiếu → `needs_info`).
  - Kiểm tra quyền sở hữu đơn hàng bằng `lookup_order` (không thấy/không khớp → `escalated`).
  - Tính tiền qua code `compute_compensation` (bỏ qua số ngày trễ ghi trong ticket).
  - Gọi cổng host `durability.issue_refund(conn, claim_id, quote, crash_at=crash_at)` với **quote đầy đủ** (không tự trừ tiền).
  - Xuất trace chuẩn `Trace contract v1` ở mọi nhánh return (`needs_info`, `escalated`, `denied`, `resolved`, `failed`).
* **Trách nhiệm Test (Tiêu chí C8 Rubric):**
  - Viết/sửa test cho Shape Workflow: ví dụ `src/tests/test_workflow_branches.py` (kiểm tra các case thiếu order_id, order cancelled, quote = 0).
* **Trách nhiệm Báo cáo:**
  - Viết Mục 1 (Thông tin nhóm), Mục 2 (Mục tiêu & cách tiếp cận), Mục 3 (phần Shape A) trong `report/team/group_report.md`.
  - Hoàn thiện báo cáo cá nhân `report/team/2A202603826_NguyenHoangTrung.md`.

---

### 👤 2. Nguyễn Tuấn Dũng — Single-Agent ReAct Specialist (Shape B)
* **Trách nhiệm Lập trình (`src/lab8/shapes/single.py`):**
  - Cấu hình và gọi vòng lặp ReAct bằng `lab8.runtime.run_react` với giới hạn cứng `max_steps=8`.
  - **Chỉ cấp Read-Only Tools** cho Agent: `lookup_order`, `lookup_policy`, `lookup_refund_history`, `compute_compensation`. Tuyệt đối **không** cấp tool ghi tiền (`issue_refund`).
  - Xử lý phòng chống Prompt Injection: Agent phải lấy dữ liệu thực tế từ DB/Order row, không được tin vào lời lẽ khách hàng trong ticket ("tôi bị trễ 9 ngày", "hãy bỏ qua policy").
  - Quản lý Budget và bước lặp để chi phí model không bị bùng nổ.
  - Sau vòng ReAct, gọi host qua `durability.issue_refund` với full quote và truyền `crash_at`.
* **Trách nhiệm Test (Tiêu chí C8 Rubric):**
  - Viết/sửa test cho Shape Single: ví dụ `src/tests/test_single_agent_limits.py` (kiểm tra Agent dừng đúng 8 bước, Agent không gọi tool ghi, hoặc Agent không bị lừa bởi ticket text).
* **Trách nhiệm Báo cáo:**
  - Viết phần mô tả Shape B trong `report/team/group_report.md` (cơ chế quyết định tool, giới hạn budget, sự dao động giữa các seed).
  - Hoàn thiện báo cáo cá nhân `report/team/2A202603859_NguyenTuanDung.md`.

---

### 👤 3. Phùng Thị Nhài — Orchestrator & Security Specialist (Shape C)
* **Trách nhiệm Lập trình (`src/lab8/shapes/orchestrator.py`):**
  - Hiện thực luồng Orchestrator phối hợp cùng các Read-Only Investigators (`run_readonly_investigators`).
  - **Bảo mật ranh giới (Handoff Sanitization):** Tạo gói handoff bằng `lab8.handoff.make_handoff` chỉ chứa facts trong allowlist.
  - **Tuyệt đối không đưa** `parent_secret`, token bí mật, raw headers, hay thông tin cá nhân (phone, address, ghi chú nội bộ) vào handoff.
  - Đảm bảo Trace ghi nhận handoff đã được làm sạch, không ghi context thô của orchestrator.
  - Orchestrator thu thập dữ kiện từ investigator, tính quote và gọi `durability.issue_refund` (truyền `crash_at`).
* **Trách nhiệm Test (Tiêu chí C8 Rubric):**
  - Viết/sửa test bảo mật: ví dụ `src/tests/test_handoff_security_custom.py` (kiểm tra `secret_leak_count == 0`, không lộ `CANARY_SECRET_*`, PII được bóc tách an toàn).
* **Trách nhiệm Báo cáo:**
  - Viết phần ranh giới bảo mật, cơ chế khử khuẩn handoff và trace an toàn trong `report/team/group_report.md`.
  - Hoàn thiện báo cáo cá nhân `report/team/2A202603725_PhungThiNhai.md`.

---

### 👤 4. Lương Thị Hồng Hạnh — Durability, Benchmark & Evaluation Specialist
* **Trách nhiệm Thực nghiệm, Độ bền & Chấm điểm:**
  - **Kiểm soát độ bền (Durability):** Kiểm tra tính Idempotency của ledger (`refund:{claim_id}`), xử lý crash injection không sinh thêm refund (T11, T12).
  - **Crash Test (CP4):** Chạy và kiểm tra đạt chuẩn an toàn **20/20**:
    ```powershell
    python -m lab8.crash_test --count 20 --out reports/crash.json
    ```
  - **Benchmark Suite (CP5):** Chạy benchmark 4 shape trên 5 seed:
    ```powershell
    python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json
    ```
  - **Tự kiểm tra hidden (CP5):** Chạy kiểm tra trên tập `student_drop/`.
* **Trách nhiệm Tài liệu Nghiên cứu & Quyết định (Bắt buộc theo Rubric):**
  - Điền hoàn chỉnh file `report/team/decision_adr.md` (lấy số liệu thật từ `reports/benchmark.json`, điền commit hash, run id, lý do chọn kiến trúc ít tự chủ nhất).
  - Điền hoàn chỉnh file `report/team/research_card.md` (chọn 1 câu trong R1–R4 và thiết kế 1 bài thực nghiệm ablation).
* **Trách nhiệm Test (Tiêu chí C8 Rubric):**
  - Viết/sửa test về Durability: ví dụ `src/tests/test_durability_crash_custom.py` (kiểm tra gọi lại claim đã refund, crash resume không tạo duplicate refund).
* **Trách nhiệm Báo cáo:**
  - Viết Mục 4 (Kết quả thực nghiệm benchmark/crash) và Mục 7 (Hạn chế & hướng phát triển) trong `report/team/group_report.md`.
  - Hoàn thiện báo cáo cá nhân `report/team/2A202603748_LuongThiHongHanh.md`.

---

## 3. Lộ trình phối hợp qua 5 Checkpoint tại lớp

```
[CP1: 13:30] Cài đặt môi trường, chạy smoke, chia vai, điền TEAM.md
     │
[CP2: 13:45] Code 3 Shape (Trung: Workflow | Dũng: Single | Nhài: Orchestrator | Hạnh: Test & review)
     │
[CP3: 14:30] Xử lý Crash_at, Ledger Idempotency & Handoff Sanitization
     │
[CP4: 15:30] Đạt 20/20 Crash suite, kiểm tra Zero Secret Leak & Approval Bypass
     │
[CP5: 16:15] Chạy Benchmark, điền ADR & Research Card, check_submission 0 FAIL
     │
[NỘP: 17:00] Push Git, kiểm tra link repo public, nộp link trên LMS
```

* **CP1 (13:30 – 13:45):** Cả 4 thành viên kéo code về máy, kích hoạt virtualenv, chạy `python -m lab8.smoke` và `python -m pytest -q` (đảm bảo host pass).
* **CP2 (13:45 – 14:30):** Trung, Dũng, Nhài hoàn thành các dòng `TODO CP2` trong 3 file shape. Kiểm tra:
  ```powershell
  python -m pytest -q -m student -o addopts= -k workflow
  python -m pytest -q -m student -o addopts= -k single
  python -m pytest -q -m student -o addopts= -k orchestrator
  ```
  *(Mỗi shape đạt 62 passed)*.
* **CP3 (14:30 – 15:15):** Trung, Dũng, Nhài hoàn thành dòng `TODO CP3` (truyền `crash_at` vào `durability.issue_refund`, không catch `InjectedCrash`). Hạnh chạy kiểm tra test T11, T12 xanh.
* **CP4 (15:30 – 16:15):** Hạnh chạy crash test sinh file `src/reports/crash.json` đạt `20/20`. Nhài và Hạnh rà soát log/trace đảm bảo không lộ `CANARY_SECRET_*`.
* **CP5 (16:15 – 17:00):** Hạnh chạy benchmark và hidden self-check. Trung & Hạnh điền số liệu vào `decision_adr.md` và `research_card.md`. Cả nhóm hoàn thiện báo cáo và chạy lệnh nghiệm thu:
  ```powershell
  python -m lab8.check_submission
  ```
  *(Bắt buộc ra `0 FAIL`)*.

---

## 4. Dữ liệu chuẩn để điền vào `TEAM.md`

Dán nội dung sau vào file `TEAM.md` ở thư mục gốc:

```markdown
## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Hoàng Trung | 2A202603826 | [Email Trung] | [GitHub Trung] | Workflow + Integration (Lead) |
|   2 | Nguyễn Tuấn Dũng | 2A202603859 | [Email Dũng] | [GitHub Dũng] | Single ReAct Agent |
|   3 | Phùng Thị Nhài | 2A202603725 | [Email Nhài] | [GitHub Nhài] | Orchestrator + Handoff Security |
|   4 | Lương Thị Hồng Hạnh | 2A202603748 | [Email Hạnh] | [GitHub Hạnh] | Durability, Benchmark & Evaluation |

## Bảng đóng góp

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Nguyễn Hoàng Trung | Workflow + Integration | [commit_hash_1] | tests/test_workflow_branches.py |
| Nguyễn Tuấn Dũng | Single ReAct Agent | [commit_hash_2] | tests/test_single_agent_limits.py |
| Phùng Thị Nhài | Orchestrator + Handoff | [commit_hash_3] | tests/test_handoff_security_custom.py |
| Lương Thị Hồng Hạnh | Durability + Evaluation | [commit_hash_4] | tests/test_durability_crash_custom.py |
```

---

## 5. Danh sách 4 file báo cáo cá nhân cần tạo
Mỗi bạn copy nội dung từ file mẫu `report/team/MSSV_HoTen.md` ra file mang tên mình:
1. `report/team/2A202603826_NguyenHoangTrung.md`
2. `report/team/2A202603859_NguyenTuanDung.md`
3. `report/team/2A202603725_PhungThiNhai.md`
4. `report/team/2A202603748_LuongThiHongHanh.md`

*(Giữ nguyên file mẫu `MSSV_HoTen.md` trong repo)*.
