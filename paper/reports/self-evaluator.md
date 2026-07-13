# Self-Evaluator Report — main.md

**Bài báo:** Reproducible Detection of AI-Generated Faces via Open Handcrafted Features on PCA-Residual Images
**File:** `D:\CPV-VIP\paper\main.md` (194 dòng)
**Khâu:** `self-evaluator` — Task #22, bước 6/6 (khâu CUỐI) trong pipeline `paper-writing-integrity.md` §6
**Khâu trước:** `ieee-q1-devil-advocate` — PASS cho venue band thật (xem `paper/reports/ieee-q1-devil-advocate.md`)
**Ngày:** 2026-07-14

---

## Quy trình đối chiếu độc lập (không chỉ tin báo cáo trước)

Trước khi chấm điểm, đã tự chạy lại — không suy đoán từ báo cáo cũ:

| # | Hạng mục | Phương pháp | Kết quả |
|---|---|---|---|
| 1 | Không bold trong Abstract | `Grep "\*\*[^*]"` toàn file 194 dòng | **0 match trong toàn file** (không chỉ Abstract — mạnh hơn yêu cầu gốc) |
| 2 | Không `\tag`/`\label`/`\ref`/`\eqref` | `Grep "\\tag\|\\label\|\\ref\|\\eqref"` toàn file | **0 match** — đối chiếu độc lập, khớp với finding của `latex-fix.md` |
| 3 | Không TODO/TBD/FIXME/placeholder-nội-dung | `Grep "TODO\|TBD\|\[FIXME\|placeholder"` (case-insensitive) | **0 match** (placeholder tên tác giả dùng quy ước "— nhóm điền", không phải các từ khóa này — xem Issues Found #1) |
| 4 | Không từ overclaim (paradigm/breakthrough/novel/SOTA/unprecedented/revolutionary) | `Grep` case-insensitive toàn file | **0 match** — xác nhận style-humanizer đã loại hết 4/4 "paradigm" và không có từ overclaim nào khác lọt vào |
| 5 | Algorithm 1 có giải thích vấn đáp-sẵn-sàng | Đọc trực tiếp dòng 69–107 (pseudocode + đoạn văn xuôi diễn giải) | **Đạt** — 13 dòng pseudocode (dòng 71–96) đi kèm giải thích từng bước ngay sau (dòng 97–107), gồm cả lý do kỹ thuật chọn `nri_uniform` thay vì `uniform` (59 vs 10 mã khả dụng) |
| 6 | Table 1 khớp số liệu gốc | Đọc trực tiếp dòng 133–139, so khớp từng ô với bảng gốc đã verify từ đầu phiên | **Khớp 100%, cả 30/30 ô** (5 hàng × 6 cột: Val/Test Acc/F1/AUC cho 5 classifier) |
| 7 | 5 sửa đổi của `ieee-q1-devil-advocate` thực sự nằm trong file | Đọc trực tiếp dòng 11, 31, 35, 141, 145, 153 | **Cả 5 đều có mặt** — xem bảng chi tiết bên dưới |
| 8 | Toàn bộ prose còn lại (Introduction, Related Work mở đầu, §4.1) chưa được đọc trực tiếp trong phiên self-evaluator | Đọc trực tiếp dòng 14–43 và 69–96 | **Đọc xong, không phát hiện vấn đề mới** — nội dung nhất quán với các phần đã verify trước đó |
| 9 | 3 báo cáo trước (`citation-guard`, `style-humanizer`, `latex-fix`) — đọc toàn văn thay vì chỉ tin kết luận | Đọc trực tiếp cả 3 file report | **Cả 3 đều PASS với phương pháp verify cụ thể** (không phải kết luận suông) — xem tóm tắt bên dưới |

### Chi tiết mục 7 — 5 sửa đổi của ieee-q1-devil-advocate

| Dòng | Nội dung kỳ vọng sau sửa | Có trong file? |
|---|---|---|
| 11 | Abstract: "86.9 percent" / "0.944" (số đã sửa đúng, khớp Table 1 max) | ✅ Có |
| 31 | "Three recent studies apply this handcrafted-plus-classical-ML recipe..." (sửa từ "Two") | ✅ Có, đúng 3 nghiên cứu [4][9][10] |
| 35 | Câu định vị khoảng trống không còn rò rỉ jargon "T1" nội bộ, không còn cross-reference gãy tới Section 5 | ✅ Có, đọc lại nguyên văn: "Closing that specific gap, not proposing a new architecture, is the contribution of this paper: a recipe-level extension of an existing representation, not a new model or problem formulation." |
| 141 | Ngưỡng AUC "roughly 0.003" (sửa từ "0.002" bị chính Table 1 vi phạm) | ✅ Có |
| 145 | Gán đúng: XGBoost thắng cả 3 test metric, LightGBM nhì sát nút dù thắng validation | ✅ Có, đọc lại nguyên văn khớp đúng Table 1 |
| 153 | Câu công khai phạm vi reproducibility mới (§6.3) | ✅ Có |

### Tóm tắt đối chiếu 3 báo cáo trước (đọc toàn văn phiên này)

- **`citation-guard.md`**: PASS — 17/17 nguồn được trích dẫn, 0 mồ côi, 0 mục thừa, 11/17 mục có sửa lỗi thực chất (tên tác giả đầy đủ, venue thiếu, định dạng DOI) với nguồn verify cụ thể (CrossRef/arXiv/WebSearch cho từng mục, không phải khẳng định chung chung). Synthesis-quality scan PASS với trích dẫn nguyên văn chứng minh (không liệt kê tuần tự). 1 finding không chặn (thứ tự đánh số theo chủ đề thay vì appearance-order) — đã có bảng ánh xạ sẵn sàng, đúng đắn khi không tự động áp dụng một phép hoán vị lớn không được yêu cầu.
- **`style-humanizer.md`**: PASS — 25 sửa đổi (4× "paradigm"→"approach"/"line of work", 20 semicolon tách câu, 1 câu mở Introduction tách burstiness), toàn bộ đếm lại bằng `grep`/`awk`/`wc` thật, không ước lượng. Xác nhận LUẬT 0 (bất biến bảo toàn nghĩa) qua đối chiếu toàn văn 194 dòng sau sửa — số liệu/công thức/citation-key/độ mạnh khẳng định/chiều so sánh đều khớp 100% với bản trước khi sửa.
- **`latex-fix.md`**: PASS — 0 sửa đổi thực sự cần thiết; 1 cảnh báo linter (dòng 45, `$$` đóng) được verify là false-positive do bug parity mở/đóng của chính script `_has_unspaced_display()`, giữ nguyên nội dung thay vì áp fix cơ học sai. Khối công thức duy nhất (dòng 43–45) xác nhận không đổi.

Không phát hiện mâu thuẫn nào giữa 4 báo cáo trước và nội dung thực tế của `main.md` tại thời điểm đọc trực tiếp phiên này.

---

## Self-Evaluation: main.md

### Results

| Dimension | Status | Issues |
|-----------|--------|--------|
| Completeness | ✅ PASS | Placeholder tên tác giả/khoa/email còn tồn đọng — đúng quy ước "không bịa tên", nhưng cần nhóm điền trước khi nộp thật (xem Issues #1) |
| Accuracy | ✅ PASS | Không phát hiện số liệu/trích dẫn/công thức bịa; mọi giới hạn (không ablation PCA-vs-raw, không multi-seed, không SOTA deep-learning baseline trực tiếp) đã được công khai đúng mức trong §6.3/§7, không claim vượt quá `notes/claims-ledger.md` C-1/C-2 |
| Token Efficiency | ✅ PASS | Toàn bộ 6 khâu pipeline đều dùng preview 5–9 dòng + đường dẫn, không dump nội dung file/report vào chat |
| Hallucination Guard | ✅ PASS | 17/17 trích dẫn verify thật (DOI/arXiv/WebSearch); mọi số trong Table 1 truy được về run thật (2 lần độc lập); không API/path bịa |

### Overall: PASS

### Issues Found

1. **[Completeness] [Low]** Tên tác giả, tên khoa/trường, và email liên hệ vẫn là placeholder (`[Author name — nhóm điền]` ×2, `[Department / University name — nhóm điền]`, `[email — nhóm điền]`, dòng 3–7). Đây KHÔNG phải lỗi bịa đặt — đúng ngược lại, là hành vi đúng theo `paper-writing-integrity.md` §1 (không bịa tên khi chưa biết tên thật). — **Fix:** nhóm điền tên thật + affiliation thật trước khi nộp; không cần chạy lại bất kỳ khâu nào khác trong pipeline vì đây không phải nội dung học thuật.
2. **[Completeness] [Low]** Thứ tự đánh số References theo nhóm chủ đề (fractal/PCA-residual → benchmark → tiền lệ phương pháp luận → nguồn nền tảng) thay vì đúng thứ tự xuất hiện lần đầu trong thân bài — đã được `citation-guard.md` §3.1 ghi nhận từ trước (không phải phát hiện mới), kèm bảng ánh xạ cũ→mới sẵn sàng áp dụng. Không phải lỗi trích dẫn sai/mồ côi/bịa — thuần túy là lựa chọn quy ước. — **Fix (tùy chọn):** nếu venue đích yêu cầu appearance-order nghiêm ngặt, áp dụng bảng ánh xạ tại `paper/reports/citation-guard.md` §3.1; nếu không, giữ nguyên đánh số theo chủ đề là hợp lệ.

Không có issue nào ở mức Medium/High/Critical. Điều kiện FAIL ("bất kỳ dimension nào có Critical issue") không xảy ra ở dimension nào.

---

## Tổng kết toàn bộ pipeline (6/6 khâu, `paper-writing-integrity.md` §6)

| # | Khâu | Verdict | Report |
|---|---|---|---|
| 1 | `paper-submission` (draft) | ✅ Hoàn tất — bản thảo 194 dòng, cấu trúc mô phỏng bài mẫu SARD_Springer | `paper/main.md` |
| 2 | `citation-guard` | ✅ PASS — 17/17 nguồn verify, 0 mồ côi | `paper/reports/citation-guard.md` |
| 3 | `style-humanizer` | ✅ PASS — 25 sửa văn phong, LUẬT 0 giữ nguyên nghĩa | `paper/reports/style-humanizer.md` |
| 4 | `latex-fix` | ✅ PASS — 0 sửa thực, 1 false-positive đã verify | `paper/reports/latex-fix.md` |
| 5 | `ieee-q1-devil-advocate` | ✅ PASS (venue band thật) — phát hiện và sửa 5 lỗi thật A–E ngay trong lượt review | `paper/reports/ieee-q1-devil-advocate.md` |
| 6 | `self-evaluator` | ✅ PASS — đối chiếu độc lập 9 hạng mục, 2 issue mức Low (không chặn) | `paper/reports/self-evaluator.md` (báo cáo này) |

**Kết luận cuối cùng: bài báo đã SẴN SÀNG cho mục tiêu venue thật (Workshop/hội nghị Q4/Scopus-index, theo `notes/claims-ledger.md` C-1/C-2).** Không có vi phạm integrity nào tồn đọng; 2 issue còn lại đều ở mức Low và không cần chặn tiến độ. Trước khi nộp thật, nhóm chỉ cần: (a) điền tên tác giả/khoa/email thật, (b) tùy chọn áp bảng ánh xạ đánh số References nếu venue đòi appearance-order nghiêm ngặt.
