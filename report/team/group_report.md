# Báo cáo nhóm — Lab 8 LogiX-VN
**Nhóm:** SpaceX — **Lớp:** L3B

## 1. Thông tin nhóm

- Tên nhóm: SpaceX
- Thành viên: Nguyễn Hoàng Trung, Nguyễn Tuấn Dũng, Phùng Thị Nhài, Lương Thị Hồng Hạnh (xem chi tiết tại `TEAM.md`)
- Commit chốt: `b1aef5f` (trùng khớp với `report/team/decision_adr.md`)

## 2. Mục tiêu và cách tiếp cận

### 2.1. Mục tiêu bài toán
Bài toán đặt ra cho LogiX-VN là xây dựng và đánh giá hệ thống xử lý claim hoàn phí vận chuyển và bồi thường hư hại hàng hóa tự động dựa trên **4 kiến trúc**:
1. **Shape A — Deterministic Workflow:** Quy trình cứng bằng mã Python.
2. **Shape B — Single ReAct Agent:** Tác tử đơn lẻ lặp qua vòng ReAct có chặn bước (tối đa 8 bước).
3. **Shape C — Orchestrator:** Nhạc trưởng điều phối các điều tra viên chỉ đọc (read-only investigators) qua gói bàn giao (handoff) khử khuẩn.
4. **Shape D — Reference Swarm:** Đàn tác tử ngang hàng phân tán (được cung cấp sẵn làm mốc đối chứng).

### 2.2. Nguyên tắc ranh giới cốt lõi
- **Tiền bạc và Quyết định ghi sổ thuộc về Code:** Số tiền hoàn được tính hoàn toàn thông qua engine luật nghiệp vụ `compute_compensation`. LLM / MockLLM tuyệt đối không quyết định số tiền hay tự ghi sổ.
- **Ranh giới an toàn của Host:** Mọi thao tác ghi sổ đều đi qua cổng duyệt `durability.issue_refund`. Cổng này đảm bảo tính Idempotent (`refund:{claim_id}`), kiểm soát trần theo đơn hàng, kiểm tra tính hợp lệ của approval và lưu vết audit `refund_committed` hoặc `policy_denied`.
- **Nguyên tắc lựa chọn kiến trúc:** Chọn kiến trúc **ít tự chủ nhất mà vẫn hoàn thành công việc** với độ tin cậy cao nhất và chi phí thấp nhất.

## 3. Giải pháp kỹ thuật

### 3.1. Hiện thực ba Shape (A, B, C)
- **Shape A (`src/lab8/shapes/workflow.py`):**
  Thực thi tuần tự các bước xác định: đọc claim bằng `get_claim_view`, kiểm tra `order_id` (nếu thiếu trả `needs_info`), kiểm tra phạm vi sở hữu đơn bằng `lookup_order` (nếu không thấy trả `escalated`). Sau đó tính quote qua `compute_compensation`. Nếu quote > 0, gọi `durability.issue_refund` với **toàn bộ quote**; nếu quote <= 0, trả `denied` mà không gọi host ghi sổ.
- **Shape B (`src/lab8/shapes/single.py`):**
  Sử dụng vòng lặp ReAct `lab8.runtime.run_react` với chặn cứng `max_steps=8`. Trong vòng lặp, tác tử chỉ được cấp quyền gọi các công cụ đọc (`lookup_order`, `compute_compensation`, `lookup_policy`). Tác tử lấy thông tin trễ từ DB order row, không bị lừa bởi lời kể của khách hàng trong ticket. Sau khi vòng lặp dừng với kết quả đề xuất, host mới là bên duy nhất thực hiện `issue_refund`.
- **Shape C (`src/lab8/shapes/orchestrator.py`):**
  Orchestrator phân rã tác vụ và đóng gói dữ kiện qua `lab8.handoff.make_handoff`. Gói bàn giao chỉ chứa các trường trong `FACT_KEYS` và danh sách công cụ chỉ đọc trong allowlist (`lookup_order`, `lookup_policy`, `compute_compensation`). Các điều tra viên (`run_readonly_investigators`) chạy độc lập không có quyền ghi. Orchestrator tổng hợp thông tin, trích xuất quote và gọi `durability.issue_refund`.

### 3.2. Bảo mật ranh giới & Trace contract v1
- **Khử khuẩn Handoff:** Hàm `make_handoff` và `sanitize` loại bỏ hoàn toàn các trường nhạy cảm như `parent_secret`, `raw_headers`, token xác thực, cũng như thông tin định danh cá nhân (số điện thoại, địa chỉ, tên hàng, ghi chú nội bộ).
- **Tuân thủ Trace contract v1:** Mọi nhánh kết thúc của cả ba shape đều xuất file trace JSON với `run_id` duy nhất và danh sách các sự kiện (`events`). Trace chỉ ghi dữ liệu đã qua allowlist, đảm bảo scanner quét sạch và không có bất kỳ chuỗi cấm `CANARY_SECRET_*` nào.

### 3.3. Độ bền dữ liệu (Durability) và Xử lý sự cố (Crash Safety)
- Ở tất cả các shape, tham số `crash_at` được chuyển tiếp vào `durability.issue_refund`.
- Không bắt ngoại lệ `InjectedCrash` mà chỉ flush trace trước khi lan truyền ngoại lệ để đảm bảo grader kiểm tra chính xác điểm crash.
- Tính Idempotency được bảo chứng bởi khóa `refund:{claim_id}` trong transaction duy nhất của SQLite, giúp resume an toàn mà không sinh thêm dòng refund nào.

## 4. Kết quả thực nghiệm

### 4.1. Bảng số liệu Benchmark 4 Shape (Từ `src/reports/benchmark.json`)
Chạy trên toàn bộ 14 claims public × 5 seeds (11, 22, 33, 44, 55) = 70 trials mỗi shape:

| Kiến trúc (Shape) | Pass Rate | Pass^5 | Seed Variance | Min Seed | Max Seed | Cost/Success (VND) | Mean Steps | P95 Steps |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Workflow (A)** | **1.000** | **1.000** | **0.000000** | **1.000** | **1.000** | **28.79** | 2.79 | 3.0 |
| **Single Agent (B)**| 1.000 | 1.000 | 0.000000 | 1.000 | 1.000 | 29.65 | 1.86 | 2.0 |
| **Orchestrator (C)**| 1.000 | 1.000 | 0.000000 | 1.000 | 1.000 | 47.85 | 3.71 | 4.0 |
| **Swarm (D)** | 0.986 | 0.929 | 0.000816 | 0.929 | 1.000 | 49.57 | 2.80 | 3.0 |

### 4.2. Kết quả kiểm tra Crash Safety (`src/reports/crash.json`)
- Đạt kết quả tuyệt đối: **`crash_safety = 20/20`**.
- Mọi điểm tiêm lỗi (`before_effect`, `after_effect_before_checkpoint`, `after_checkpoint`) đều được khôi phục chính xác: đúng 1 dòng ledger và đúng 1 audit `refund_committed`.

### 4.3. Quyết định kiến trúc
- **Shape được chọn:** **`workflow`**.
- **Lý do:** Đáp ứng trọn vẹn cả ba tiêu chí: Pass rate cao nhất (100%), độ ổn định tuyệt đối (Variance = 0), và chi phí vận hành thấp nhất (28.79 VND so với 49.57 VND của Swarm). Xem chi tiết tại `report/team/decision_adr.md`.

## 5. Khó khăn và cách xử lý

1. **Vấn đề trần hoàn tiền theo đơn (T13 & T14):**
   - *Khó khăn:* Ban đầu dễ mắc lỗi tự trừ tiền đã hoàn trong shape trước khi gọi host, dẫn đến việc host trừ thêm một lần nữa và làm sai lệch số tiền của T14.
   - *Giải pháp:* Truyền nguyên vẹn **quote đầy đủ** vào `durability.issue_refund`. Cổng host sẽ tự động đọc `order_refunded_vnd` và xử lý phần chênh lệch một cách nhất quán.
2. **Đảm bảo không rò rỉ Canary Secret qua Trace:**
   - *Khó khăn:* Việc ghi log `claim_row` hoặc `order_row` thô để debug dẫn tới vi phạm must-pass do dính secret hoặc PII.
   - *Giải pháp:* Tuyệt đối chỉ sử dụng các hàm adapter `get_claim_view` và `lookup_order`, đồng thời bọc payload qua `safe_dump` đã khử khuẩn.

## 6. Tổng hợp đóng góp

| Thành viên | MSSV | Vai trò chính | Commit | Đóng góp kỹ thuật |
| :--- | :---: | :--- | :---: | :--- |
| Nguyễn Hoàng Trung | 2A202603826 | Lead, Workflow & Integration | `1c75422` | Viết `workflow.py`, thiết lập repo, `test_workflow_custom.py` |
| Nguyễn Tuấn Dũng | 2A202603859 | Single ReAct Agent | `eb1af72` | Viết `single.py`, chặn 8 steps, `test_single_custom.py` |
| Phùng Thị Nhài | 2A202603725 | Orchestrator & Security | `b65a5ad` | Viết `orchestrator.py`, sanitize handoff, `test_orchestrator_custom.py` |
| Lương Thị Hồng Hạnh | 2A202603748 | Durability, Benchmark & Eval | `b5125b5` | Chạy crash suite 20/20, benchmark, `decision_adr.md`, `test_durability_custom.py` |

## 7. Hạn chế và hướng cải thiện

- **Giới hạn mô phỏng:** Nghiên cứu sử dụng `MockLLM` dựa trên băm sha256 và biểu thức chính quy. Độ trễ thực tế chưa được phản ánh (`latency: unavailable`). Chi phí token là giá trị ước lượng theo bảng giá quy định.
- **Điều kiện mở rộng:** Nếu hệ thống tiếp nhận các khiếu nại dạng ảnh chụp hóa đơn giao nhận mờ, khiếu nại bằng văn bản tự do không theo cấu trúc chuẩn, hoặc yêu cầu thương lượng động, kiến trúc Orchestrator kết hợp multimodal vision agent sẽ là ứng viên cần được xem xét thay thế.

## 8. Tài liệu tham khảo

1. Google Research (2026), *Towards a Science of Scaling Agent Systems*.
2. MAST, NeurIPS (2025), *Why Do Multi-Agent LLM Systems Fail?*.
3. LogiX-VN Architecture & Contracts Documentation (`docs/architecture.md`, `docs/contracts.md`, `docs/business_rules.md`).
