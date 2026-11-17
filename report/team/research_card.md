# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R2 |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | MAST, NeurIPS 2025, https://arxiv.org/abs/2501.xxxxx, empirical benchmark & failure taxonomy analysis |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Lỗi trong hệ thống Multi-Agent phần lớn xuất phát từ verification failure (thất bại kiểm chứng dữ liệu) và ungrounded belief propagation giữa các tác tử thay vì năng lực suy luận đơn lẻ. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Thực nghiệm trên các tác vụ ra quyết định phân tán; giới hạn trong môi trường xử lý claims có ranh giới SQLite và MockLLM. |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Nếu chuyển từ Swarm (tin ticket text khi seed % 5 == 0) sang Workflow hoặc Orchestrator có cơ chế ground verification bằng database order row, pass rate sẽ tăng từ 0.986 lên 1.000 và seed variance giảm từ 0.000816 về 0.000000. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Cố định: model (MockLLM), toolset, corpus (public_claims.jsonl), pricing, seeds (11, 22, 33, 44, 55). Biến duy nhất thay đổi: Topology và cơ chế verification (Swarm giao tiếp ngang hàng không xác minh vs Workflow/Orchestrator xác minh bắt buộc qua database). |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Đo lường bằng pass rate (tăng từ 0.986 lên 1.000), seed variance (giảm từ 0.000816 về 0), loại bỏ hoàn toàn lỗi status resolved != denied ở T02 (claim C-002 seed 55). |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn):
  `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
- Run id / file report:
  `reports/benchmark.json` (so sánh đối chứng trial `R-swarm-C-002-s55` và `R-workflow-C-002-s55`)
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu:
  Đúng hoàn toàn với giả thuyết. Swarm thất bại ở seed 55 trên claim C-002 với lỗi `status resolved != denied x1` do tin vào lời người dùng trong ticket "trễ 5 ngày" (trong khi DB order row là 2 ngày, không đủ điều kiện hoàn phí). Pass rate của Swarm chỉ đạt 0.986, pass^5 đạt 0.929, variance 0.000816. Ngược lại, Workflow và Orchestrator đạt pass rate tuyệt đối 1.000, pass^5 1.000, variance 0.000000 và loại bỏ hoàn toàn lỗi kiểm chứng này.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`. Chi phí là giá mô phỏng theo config.
