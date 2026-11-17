# Báo cáo cá nhân — 2A202603725_PhungThiNhai

## 1. Thông tin thành viên

- Họ tên: Phùng Thị Nhài
- MSSV: 2A202603725
- Email: nhaipt342k4@gmail.com
- GitHub: nhaipt342K4

## 2. Phần việc phụ trách

- Chuyên trách nghiên cứu và lập trình Shape C (Orchestrator + Read-only Investigators): `src/lab8/shapes/orchestrator.py`.
- Bảo mật ranh giới hệ thống: dùng allowlist có sẵn của host (`lab8.handoff.make_handoff` và `sanitize`) để dựng gói handoff đã khử khuẩn cho investigator, và chỉ ghi handoff đã sanitize vào trace (không ghi parent context).
- Đảm bảo rà soát không rò rỉ secret (`CANARY_SECRET_*`) và thông tin định danh cá nhân (PII) qua trace.
- Viết test suite bảo mật: `src/tests/test_orchestrator_custom.py`.
- Viết phần bảo mật ranh giới và sanitization trong báo cáo nhóm `report/team/group_report.md`.

## 3. Đóng góp cụ thể

- Commit chính: `b65a5ad` ("feat(orchestrator): implement Shape C orchestrator, handoff sanitization and security tests").
- Test đã thêm: `src/tests/test_orchestrator_custom.py` (6 hàm test, 20 trial) gồm: trace không chứa secret/PII trên **toàn bộ 14 claim public**; đủ các nhánh `resolved` (C-003, C-010), `needs_info` (C-004), `escalated` (C-005), `denied` do quote = 0 với ticket chứa prompt injection (C-009), và `denied` do host từ chối approval hết hạn nhưng `proposal_amount` vẫn là quote đầy đủ (C-007).
- Quyết định kỹ thuật:
  - Chỉ cho phép investigator sử dụng các công cụ trong allowlist chỉ đọc (`lookup_order`, `lookup_policy`, `compute_compensation`).
  - Gói handoff chỉ giữ các field trong `ALLOWED_FIELDS`; `parent_secret`, `raw_headers` và mọi chuỗi `CANARY_SECRET_*` bị loại hoặc bị chặn (`HandoffError`) trước khi chuyển giao. Không dùng LLM để tóm tắt parent context vì tóm tắt không phải là redaction.
  - Orchestrator đọc claim bằng các cột cần thiết (`claim_id, principal_id, order_id, ticket`), không `SELECT *`, nên `parent_secret` không bao giờ được nạp vào.
  - Truyền **quote đầy đủ** từ `compute_compensation` vào `durability.issue_refund` để host tự trừ phần đã hoàn của đơn (T13, T14); truyền `crash_at` và không bắt `InjectedCrash` (T12).

## 4. Bằng chứng

- Link commit: `b65a5ad`
- Tên test (trong `src/tests/test_orchestrator_custom.py`): `test_orchestrator_sanitizes_handoff_and_no_leak`, `test_orchestrator_resolves_valid_damage_claim`, `test_orchestrator_missing_order_id_needs_info`, `test_orchestrator_other_principal_escalated`, `test_orchestrator_ignores_injection_in_ticket`, `test_orchestrator_expired_approval_denied_with_full_quote`, `test_orchestrator_trace_clean_for_every_claim`.
- Kết quả kiểm tra: 62/62 student test pass trên Shape Orchestrator; 20/20 test trong `test_orchestrator_custom.py` pass (quét 30 giá trị PII: phone, address, internal note); cổng host `python -m pytest -q` xanh.
- Benchmark (`src/reports/benchmark.json`, seed 11,22,33,44,55): 70/70 trial đạt, pass rate 1.000, pass^5 1.000, seed variance 0.000000, cost/success ≈ 47.85 VND (chi phí mô phỏng), mean steps ≈ 3.71; số lượng secret leak = 0 và approval bypass = 0.
- Run ID dẫn chứng: `R-orchestrator-C-001-s11`.

## 5. Công cụ AI đã dùng

- Công cụ: Antigravity AI Assistant.
- Mục đích: Hỗ trợ cấu hình tích hợp giữa orchestrator và runner điều tra viên chỉ đọc.
- Cách tự kiểm chứng:
  - Chạy `python -m pytest -q -m student -o addopts= -k orchestrator` (62 passed) và `python -m pytest -q` (cổng host xanh).
  - Mở các file trace trong `src/traces/` (ví dụ `R-orchestrator-C-001-s11.json`), tìm chuỗi `CANARY_SECRET_`, số điện thoại, địa chỉ để chắc chắn không có rò rỉ.
  - Đối chiếu code với `docs/contracts.md` và `docs/business_rules.md` (status từng nhánh, quote đầy đủ, `crash_at`).

## 6. Tự đánh giá

- **Điều em đã hiểu:**
  - Vì sao investigator chỉ được dùng tool đọc, còn chỉ host (`durability.issue_refund`) mới được ghi tiền: tách quyền để một chỗ bị lừa không làm mất tiền.
  - Vì sao trace cũng là ranh giới bảo mật: grader quét trace để tìm secret/PII, nên trace chỉ được ghi dữ liệu đã qua allowlist.
  - Vì sao phải truyền quote đầy đủ cho host: host tự trừ phần đơn đã được hoàn, shape tự trừ trước sẽ bị trừ hai lần (T14).
  - Vì sao không được bắt `InjectedCrash`: test T12 cần crash xảy ra thật để kiểm resume không tạo refund thứ hai.
- **Điều em đã tự kiểm tra:** đọc lại các test trong `src/tests/test_orchestrator_custom.py` và mở file trace trong `src/traces/` để xem tận mắt trace không chứa `CANARY_SECRET_`, số điện thoại hay địa chỉ. Em bám sát tiến độ nhóm trong suốt buổi lab.
- **Hạn chế:**
  - Orchestrator có một lần gọi MockLLM `parse` trên ticket nhưng không dùng kết quả, làm cost/success cao hơn workflow (≈ 47.85 so với ≈ 28.79 VND). Em giữ nguyên để không làm đổi số benchmark đã ghi trong ADR; hướng cải thiện là bỏ lời gọi này rồi chạy lại benchmark.
  - Em còn phụ thuộc khá nhiều vào công cụ AI khi viết code, cần tự đọc lại kỹ hơn.
  - Em chưa giải thích chắc được vì sao tóm tắt bằng LLM không thay được allowlist, và chưa tự trình bày trọn vẹn luồng orchestrator từ đầu đến cuối; đây là hai phần em cần tìm hiểu thêm.
- **Tự chấm:** Hoàn thành phần việc được giao, nhưng còn một số hạn chế ở trên.
