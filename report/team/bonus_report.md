# Bonus report: B3

- Topic + nguồn (tên, năm, slide): B3 · Verifier/aggregator chống khuếch đại lỗi (Google Research 2026, slide 17, 22, 42)
- CLAIM của nguồn (1 câu): Các tác tử hoạt động độc lập có thể khuếch đại sai lệch lên tới 17.2×; việc bổ sung cơ chế kiểm chứng (Evaluator–Optimizer / Reflection) dạng tập trung bằng code giúp dập tắt lan truyền niềm tin sai (ungrounded belief propagation) và đưa tỷ lệ lỗi giảm xuống 4.4× hoặc thấp hơn.
- BOUNDARY (model / dataset / setup): Áp dụng trong bài toán xử lý claim LogiX-VN với ranh giới SQLite và MockLLM; giả định môi trường kiểm chứng có quyền đọc dữ liệu có cấu trúc từ database.
- HYPOTHESIS trên LogiX: Bổ sung một bước verifier bằng code (`bonus/swarm_verified.py`) để đối chiếu delay và facts từ database trước khi ghi sổ sẽ khắc phục triệt để điểm yếu của Swarm ở seed 55, nâng pass rate từ 0.986 lên 1.000 và triệt tiêu phương sai (variance từ 0.000816 về 0.000000).
- Biến cố định / biến thay đổi:
  + Cố định: model (MockLLM), toolset, corpus (public_claims.jsonl 14 claims), pricing, seeds (11, 22, 33, 44, 55).
  + Thay đổi: Thêm bước kiểm chứng có cấu trúc (code verifier) can thiệp trước khi ra quyết định quote cuối cùng và ghi nhận sự kiện `verifier_override`.
- Lệnh tái lập (copy-paste được):
  `python -m lab8.benchmark --shapes workflow,swarm,swarm_verified --extra-shape swarm_verified=bonus.swarm_verified:run_claim --seeds 11,22,33,44,55 --out reports/bonus_benchmark.json`
- File report + run id: `src/reports/bonus_benchmark.json`, run id dẫn chứng: `R-swarm_verified-C-002-s55`.

## Kết quả
Số liệu lấy từ file `src/reports/bonus_benchmark.json` (70 trials mỗi shape):

| Shape | Pass Rate | Pass^5 | Seed Variance | Min | Max | Cost/Success (VND) | Mean Steps | P95 Steps | Lỗi hay gặp |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `workflow` | 1.000 | 1.000 | 0.000000 | 1.000 | 1.000 | 28.79 | 2.79 | 3.0 | 0 lỗi |
| `swarm` | 0.986 | 0.929 | 0.000816 | 0.929 | 1.000 | 49.57 | 2.80 | 3.0 | status resolved != denied x1 (C-002 s55) |
| `swarm_verified` | **1.000** | **1.000** | **0.000000** | **1.000** | **1.000** | 57.29 | 3.74 | 4.0 | 0 lỗi |

Kiểm tra an toàn:
- Secret leak count: 0
- Approval bypass count: 0
- Số lần verifier override: 1 lần tại C-002 seed 55 (phát hiện claim trễ 5 ngày do model tin ticket, đối chiếu DB chỉ trễ 2 ngày -> override về 2 ngày -> quote 0 -> denied).

## Kết luận
Ủng hộ hoàn toàn giả thuyết. Việc đưa code verifier vào Swarm đã phục hồi toàn bộ độ tin cậy của hệ thống (pass rate đạt 100%, pass^5 đạt 100%, variance về 0).
Tuy nhiên, phát hiện cốt lõi từ thực nghiệm này là: **Khi verifier bằng code đã làm toàn bộ việc kiểm chứng dữ liệu thực tế và quyết định số tiền, bản thân kiến trúc Swarm trở nên thừa thãi** và gây lãng phí chi phí đáng kể (57.29 VND so với 28.79 VND của Workflow - đắt gần gấp đôi). Do đó, kết luận của nhóm càng được củng cố: Deterministic Workflow vẫn là kiến trúc ưu tiên số 1 theo nguyên tắc "ít tự chủ nhất mà làm được việc".
Điều kiện làm đảo ngược kết luận: Khi bài toán đòi hỏi suy luận trên các dữ liệu phi cấu trúc (ví dụ: hình ảnh hóa đơn viết tay, lý do bất khả kháng phức tạp) mà code rule thông thường không kiểm chứng được, khi đó sự trao đổi đa tác tử mới có giá trị bù đắp cho chi phí tăng thêm.

## Giới hạn
- MockLLM là mô hình giả lập dựa trên SHA256 và regex, chưa mô phỏng độ trễ thực tế (`latency: unavailable`).
- Chi phí token là mô phỏng theo bảng giá quy định.
- Số lượng claim trên tập public gồm 14 ca; cần tiếp tục kiểm chứng trên các tập dữ liệu lớn và đa dạng hơn trong sản xuất.
