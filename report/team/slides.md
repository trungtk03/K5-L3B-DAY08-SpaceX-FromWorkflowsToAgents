---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #0f172a
color: #f8fafc
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 40px;
  }
  h1 {
    color: #38bdf8;
  }
  h2 {
    color: #818cf8;
    border-bottom: 2px solid #334155;
    padding-bottom: 8px;
  }
  table {
    font-size: 0.75rem;
    width: 100%;
  }
  th {
    background-color: #1e293b;
    color: #38bdf8;
  }
  td {
    background-color: #0f172a;
    border: 1px solid #334155;
  }
  .highlight {
    color: #4ade80;
    font-weight: bold;
  }
  .badge {
    background: #1e293b;
    border: 1px solid #38bdf8;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
  }
---

# LAB 8: FROM WORKFLOWS TO AGENTS
### LogiX-VN: Một Task Hoàn Phí, Bốn Kiến Trúc

**Nhóm:** SpaceX | **Lớp:** L3B  
**Thành viên:**
- Nguyễn Hoàng Trung (2A202603826) — Workflow & Lead
- Nguyễn Tuấn Dũng (2A202603859) — Single ReAct Agent
- Phùng Thị Nhài (2A202603725) — Orchestrator & Security
- Lương Thị Hồng Hạnh (2A202603748) — Durability & Benchmark

---

## 1. Bài toán & 3 Ranh giới An toàn Cốt lõi

- **Bài toán LogiX-VN:** Tự động hóa xử lý claim hoàn phí ship & bồi thường hàng vỡ theo hợp đồng và điều lệ bồi thường.
- **Ranh giới an toàn tuyệt đối:**
  1. **Tiền do Code quyết định:** Model chỉ đọc và tóm tắt. Code (`compute_compensation`) là nơi duy nhất tính tiền bồi thường.
  2. **Host quản lý ghi sổ cái:** Cổng `durability.issue_refund` là chốt chặn duy nhất kiểm soát duyệt chi, trần theo đơn và ghi ledger SQLite.
  3. **Cô lập bí mật & PII:** Handoff khử khuẩn chỉ truyền allowlist; trace tuyệt đối không lộ `CANARY_SECRET_*`, token hoặc SĐT, địa chỉ.

---

## 2. Bốn Kiến Trúc Trên Cùng Một Chữ Ký `run_claim`

- **Shape A (Workflow):** Quy trình xác định tuần tự bằng code Python. Kiểm tra điều kiện cứng, tính tiền và gọi host.
- **Shape B (Single Agent):** Vòng lặp ReAct chặn cứng 8 bước. Chỉ cấp công cụ đọc. Bỏ qua các chỉ dẫn giả mạo trong ticket.
- **Shape C (Orchestrator):** Điều phối các điều tra viên chỉ đọc qua gói bàn giao (Handoff) khử khuẩn. Host là bên ghi duy nhất.
- **Shape D (Swarm - Reference):** Đàn tác tử ngang hàng. Có điểm yếu cố hữu ở seed 55: tin lời người dùng trong ticket thay vì DB.

---

## 3. Bảng Kết Quả Thực Nghiệm Benchmark

*Chạy trên 14 claims public × 5 seeds = 70 trials mỗi shape:*

| Kiến trúc (Shape) | Pass Rate | Pass^5 | Seed Variance | Cost / Success | Mean Steps | Lỗi |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Workflow (A)** | **1.000** | **1.000** | **0.000000** | **28.79 đ** | 2.79 | **0 lỗi** |
| **Single Agent (B)** | **1.000** | **1.000** | **0.000000** | 29.65 đ | 1.86 | 0 lỗi |
| **Orchestrator (C)** | **1.000** | **1.000** | **0.000000** | 47.85 đ | 3.71 | 0 lỗi |
| **Swarm (D - Ref)** | 0.986 | 0.929 | 0.000816 | 49.57 đ | 2.80 | Fail C-002 seed 55 |

- **Crash Safety:** **20/20** | **Secret Leak:** **0** | **Approval Bypass:** **0**

---

## 4. Quyết Định Kiến Trúc (ADR)

### Nhóm chọn: **Shape A — Deterministic Workflow**

1. **Độ tin cậy tuyệt đối:** Pass rate 100%, Pass^5 đạt 100%, phương sai bằng 0. Loại bỏ hoàn toàn nguy cơ ảo giác từ model.
2. **Hiệu quả kinh tế cao nhất:** Chi phí chỉ **28.79 VND**, rẻ hơn 40% so với Orchestrator và rẻ hơn 72% so với Swarm.
3. **Triết lý thiết kế:** *"Chọn kiến trúc ít tự chủ nhất mà vẫn làm được việc"*.
4. **Điều kiện đảo chiều:** Chỉ chuyển sang Multi-Agent khi dữ liệu đầu vào là phi cấu trúc phức tạp mà rule-engine không xử lý được.

---

## 5. Độ Bền (Durability) & Bảo Mật Hệ Thống

- **Chống ghi trùng tiền (Idempotency):**
  - Khóa `refund:{claim_id}` trong transaction SQLite `BEGIN IMMEDIATE`.
  - Resume sau crash: nhận diện effect đã tồn tại, trả về `idempotent_replay`.
- **Trần hoàn tiền theo đơn (T13, T14):**
  - Truyền **quote đầy đủ** vào host; host tự trừ số tiền đã hoàn trước đó (`order_refunded_vnd`), tránh lỗi trừ 2 lần.
- **Trace Contract v1:**
  - Định dạng chuẩn JSON có `run_id` và `events`. Quét sạch toàn bộ `CANARY_SECRET_*` và thông tin định danh khách hàng.

---

## 6. Mở Rộng Nghiên Cứu: Bonus B3 (Swarm Verified)

- **Cơ sở khoa học:** Google Research 2026 — Agent tự do khuếch đại sai lệch tới **17.2×**.
- **Giải pháp:** Xây dựng biến thể `swarm_verified` có bước Verifier bằng code kiểm tra đối chiếu dữ liệu DB trước khi quote.
- **Kết quả thực nghiệm:**
  - Pass rate của Swarm tăng từ **0.986 ➔ 1.000** (khắc phục hoàn toàn lỗi seed 55).
  - Phương sai giảm từ **0.000816 ➔ 0.000000**.
  - **Bài học rút ra:** Chi phí bị đội lên **57.29 VND**. Khi code verifier đã làm toàn bộ việc đúng, việc giữ lại Swarm trở nên lãng phí.

---

## 7. Tổng Kết & Phân Công Đóng Góp

- **Nghiệm thu Grader:** `python -m lab8.check_submission` ➔ **0 FAIL, 0 WARN**.
- **Đóng góp của 4 thành viên:**
  - **Nguyễn Hoàng Trung:** Setup repo, Shape A (`workflow.py`), test `test_workflow_custom.py`.
  - **Nguyễn Tuấn Dũng:** Shape B (`single.py`), ReAct 8 bước, test `test_single_custom.py`.
  - **Phùng Thị Nhài:** Shape C (`orchestrator.py`), Handoff sanitize, test `test_orchestrator_custom.py`.
  - **Lương Thị Hồng Hạnh:** Durability 20/20, Benchmark, ADR, Bonus B3, test `test_durability_custom.py`.

---

# CẢM ƠN THẦY CÔ VÀ CÁC BẠN ĐÃ LẮNG NGHE!
### Nhóm SpaceX sẵn sàng cho phần Q&A
