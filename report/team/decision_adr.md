# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: b1aef5f
- Run id dẫn chứng: R-workflow-C-001-s11
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000-1.000 / 0.000000
- Cost per success (mô phỏng, VND): 28.79
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: 0 / 0

## Vì sao shape này

So sánh trên cùng corpus 14 claims x 5 seeds (70 trials) và cùng MockLLM, shape `workflow` đạt pass rate tuyệt đối 1.000, pass^5 đạt 1.000 với phương sai seed variance bằng 0.000000. Đồng thời, workflow có cost per success thấp nhất (28.79 VND so với 29.65 của single, 47.85 của orchestrator, và 49.57 của swarm). Kiến trúc này tuân thủ nguyên tắc "ít tự chủ nhất mà vẫn làm được việc": logic kiểm tra điều kiện, tra cứu đơn hàng và tính tiền hoàn toàn thuộc về mã nguồn xác định (deterministic code), loại bỏ hoàn toàn nguy cơ ảo giác hoặc bị ảnh hưởng bởi prompt injection từ người dùng.

## Có đáng đổi lấy multi-agent không

Không đáng đổi. Dữ liệu benchmark thực tế cho thấy Swarm tham chiếu không những có chi phí cao hơn 72% (49.57 VND vs 28.79 VND) mà còn có phương sai seed variance (0.000816), bị rớt pass rate xuống 0.986 (pass^5 là 0.929 do lỗi ở seed 55 trên claim C-002 khi model tin dữ liệu trễ trong ticket thay vì database). Điều kiện duy nhất để quyết định đảo chiều sang multi-agent là khi bài toán mở rộng sang các nhiệm vụ phi cấu trúc, đòi hỏi phân rã đa mục tiêu phức tạp hoặc đối soát tài liệu mờ (unstructured evidence) vượt quá khả năng xử lý của deterministic rule engine.

## Trace và bằng chứng

Trace của nhóm ghi nhận các event cấu trúc tối giản: `lookup_order`, `quote`, `decision`, và `crash` (khi kiểm thử lỗi). Các field nhạy cảm cố ý **không ghi** bao gồm: `parent_secret`, token `Authorization` (`raw_headers_json`), thông tin nhận dạng cá nhân PII (số điện thoại, địa chỉ, tên hàng hóa chi tiết, ghi chú nội bộ `CANARY_INTERNAL_*`). Nếu trace nằm ngoài tầm quét của scanner tự động, đội security chứng minh hệ thống an toàn bằng cách: (1) Kiểm toán kiến trúc: mọi dữ liệu vào ra qua ranh giới agent đều qua lớp bọc allowlist (`get_claim_view`, `lookup_order` chỉ chọn cột an toàn, loại bỏ SELECT *), (2) Unit tests kiểm tra asserting `CANARY_SECRET_` và regex PII không bao giờ xuất hiện trong artifact/trace blob, và (3) Static analysis chặn việc ghi các trường ngoài allowlist vào log/trace.

## Giới hạn

MockLLM là mô hình giả lập đơn giản dựa trên SHA256 và regex, không phản ánh độ trễ thực tế (`latency: unavailable`) và độ bất định của các LLM sản xuất thương mại. Chi phí token là mô phỏng theo bảng giá quy định trong `config/pricing.yaml`. Kết quả không bị sửa tay để làm tròn mà phản ánh 100% dữ liệu do công cụ benchmark và crash suite sinh ra.
