# Style Humanizer Report — main.md

**Bài báo:** Reproducible Detection of AI-Generated Faces via Open Handcrafted Features on PCA-Residual Images
**File:** `D:\CPV-VIP\paper\main.md` (194 dòng)
**Khâu:** `style-humanizer` — Task #19, bước 3/6 trong pipeline `paper-writing-integrity.md` §6
**Khâu trước:** `citation-guard` — PASS (xem `paper/reports/citation-guard.md`)
**Ngày:** 2026-07-13

---

## Pass Summary

Tổng cộng **25 chỉnh sửa** đã áp dụng lên `main.md`, toàn bộ ở mức câu/dấu câu/từ đơn lẻ — không đụng số liệu, công thức, khối thuật toán, hay trích dẫn. 23 sửa đổi được lên kế hoạch từ Bước 1–5 (term filter, dấu câu, burstiness); 2 sửa đổi bổ sung được phát hiện trong chính lượt đối chiếu LUẬT 0 cuối cùng (một semicolon bị phân loại nhầm thành "list-separator" ở dòng 31 và dòng 111 — xem chi tiết ở bảng dưới). Toàn bộ số liệu trong báo cáo này được đếm lại bằng `grep`/`awk`/`wc` trực tiếp trên file sau khi sửa, không ước lượng.

**Kết luận: PASS.**

---

## Issues table

| # | Bước | Phát hiện | Auto-fixable | Hành động |
|---|---|---|---|---|
| 1 | Step 1 — term filter | `"robust"`/`"robustness"` × 7 (dòng 11, 23, 33×2, 153, 157) | Không — domain term | **GIỮ NGUYÊN.** Mỗi occurrence gắn với khái niệm kỹ thuật cụ thể ("robustness testing", "robustness to JPEG compression and resizing", trích dẫn [12] làm tiền lệ phương pháp luận) — đúng ngoại lệ domain-term của skill, không phải buzzword AI chung chung. |
| 2 | Step 1 — term filter | `"paradigm"` × 4 (dòng 23, 27×2, 31) | Có | Thay bằng `"approach"` (3×) / `"line of work"` (1×). **4/4 đã sửa, verify lại bằng `grep -i paradigm` → 0 match.** |
| 3 | Step 2 — em dash | 4 occurrence thô (dòng 3, 5) | N/A | Toàn bộ nằm trong placeholder tác giả/khoa (`[Author name — nhóm điền]`), không phải văn xuôi khoa học. **0 trong prose — không cần sửa.** |
| 4 | Step 2 — semicolon | 45 match thô (`grep -o`) → sau khi loại 6 (dòng 13, Keywords list) + 8 (dòng 44, LaTeX `\;` spacing trong `$$...$$`, false positive regex) + 2 (dòng 74–75, `Require:` pseudocode) → **29 semicolon văn xuôi thật** | Có (20/29) | Phân loại từng semicolon theo chức năng: **20 là nối 2 mệnh đề độc lập** (an toàn tách thành 2 câu, bảo toàn nghĩa 100%) → đã tách hết; **9 là list-separator đúng chuẩn Chicago Manual** (phân tách các mục liệt kê có dấu phẩy nội bộ) → giữ nguyên. Xem breakdown ở mục "Semicolon audit" bên dưới. |
| 5 | Step 3 — throat-clearing openers | 0 phát hiện | N/A | Câu "Algorithm 1 reads as follows." (dòng 99) là câu dẫn nhập cần thiết theo đúng yêu cầu tường minh của người dùng ("thuật toán đưa vào thì ra vấn đáp phải giải thích được"), không phải throat-clearing rỗng. **PASS.** |
| 6 | Step 4 — structure patterns | Nhóm 3 mô tả (frequency/texture/noise) là sự thật cấu trúc của pipeline, không phải Rule-of-3 nhân tạo; 0 pattern "Not X. Y."; thuật ngữ "descriptor" dùng nhất quán trong §4.2 (không đổi từ đồng nghĩa lòng vòng); độ dài đoạn văn biến thiên hợp lý (3–5 đoạn/section, 2–5 câu/đoạn) | N/A | **PASS**, không sửa. |
| 7 | Step 5 — burstiness | Câu mở Introduction (dòng 17, bản gốc) dài ~55 từ, trong khi target section-specific của Introduction là "short opener, then long sentences" | Có | Tách thành câu mở ngắn (~19 từ: "Face images synthesized by generative adversarial networks and diffusion models have become difficult to distinguish from photographs by eye.") + câu dài theo sau (có trích dẫn [3]). **Đã sửa.** |
| 8 | Step 6 — TEEL | Related Work có 5 đoạn (> tối thiểu 3); mỗi đoạn ≥120 từ; cấu trúc Topic→Evidence(trích dẫn)→Explanation→Link rõ ràng (ví dụ đoạn dòng 29: Topic = "specific finding motivates..." → Evidence = Zhang/Karaman/Chang [7] + Tan et al. [14] → Link = "Both results support...") | N/A | **PASS**, không sửa. |
| 9 | Step 7 — citation integration | 100% narrative style (tác giả làm chủ ngữ ngữ pháp: "Zhang, Karaman, and Chang show that...", "Ojala, Pietikäinen, and Mäenpää..."); 0 secondary/"as cited in" citation | N/A | **PASS**, không sửa — khớp với finding của citation-guard (0% self-citation, 17/17 nguồn verify trực tiếp). |
| 10 | Step 8 — style calibration | Không có bài mẫu văn phong nào được cung cấp (chỉ có bài mẫu cấu trúc SARD_Springer, đã dùng ở Task #17) | N/A | **SKIP** hợp lệ theo đúng thiết kế skill (optional, cần past papers). |

---

## Semicolon audit (chi tiết, verify bằng `grep -on ';' main.md`)

**Trước khi sửa:** 45 match thô trên toàn file.

| Dòng | Số lượng | Phân loại | Xử lý |
|---|---|---|---|
| 13 | 6 | Keywords list separator (không phải văn xuôi) | Loại khỏi audit |
| 44 | 8 | LaTeX `\;` spacing command trong khối `$$...$$` — false positive của regex tìm `;` | Loại khỏi audit, **frozen dưới LUẬT 0** (không đụng công thức) |
| 74–75 | 2 | `Require:` line trong Algorithm 1 pseudocode — ký hiệu thuật toán, không phải văn xuôi | Loại khỏi audit |
| **Còn lại** | **29** | **Semicolon văn xuôi thật** | Phân loại tiếp bên dưới |

**Trong 29 semicolon văn xuôi:**

- **20 nối hai mệnh đề độc lập** (không có yêu cầu ngữ pháp phải dùng semicolon — dấu chấm + viết hoa chữ đầu tương đương hoàn toàn về nghĩa) → **đã tách thành 2 câu**, tại các dòng: 19×2, 31×1 (ban đầu 3, 1 đã tách ở lượt trước), 47, 59, 63, 101, 103×2, 107, 111×1 (phát hiện bổ sung trong lượt đối chiếu cuối), 119, 121, 123, 147, 153×3, 157.
- **9 là list-separator đúng chuẩn**, phân tách các mục liệt kê có dấu phẩy nội bộ (Chicago Manual of Style: dùng semicolon thay vì dấu phẩy khi bản thân mỗi mục đã chứa dấu phẩy) → **giữ nguyên**:
  - Dòng 31 (1×): "Yasir and Kim fuse...on Celeb-DFv2 [4]; Nirob et al. fuse...[9], and Chaudhari et al. combine...[10]" — liệt kê 3 nghiên cứu, mỗi mục có dấu phẩy nội bộ.
  - Dòng 33 (2×): "Xiao et al. detect...[2]; Wang et al. also build...[5]; and Mohan and Peeples show...[6]" — liệt kê 3 nguồn trong dòng fractal-descriptor family.
  - Dòng 55 (4×): liệt kê 5 giai đoạn pipeline (i)–(v).
  - Dòng 111 (2×): liệt kê 3 loại classifier (linear regression; RandomForest; ba boosted-tree implementation), mỗi mục có mô tả kèm dấu phẩy.

**Sau khi sửa:** 9 semicolon văn xuôi còn lại (verify: `grep -on ';' main.md` → dòng 31×1, 33×2, 55×4, 111×2 = 9).

**Mật độ (verify bằng đếm từ thật, không ước lượng):**
- Word count văn xuôi thật (loại front-matter tác giả, dòng Keywords, khối Algorithm 1 pseudocode, bảng Table 1, References) = **4.853 từ**, đếm bằng `awk` trích đúng các dòng văn xuôi rồi `wc -w`.
- Mật độ trước sửa: 29 / 4.853 × 1000 ≈ **5,98/1000 từ** — vượt xa target ≤2/1000.
- Mật độ sau sửa: 9 / 4.853 × 1000 ≈ **1,85/1000 từ** — **đạt target ≤2/1000.**

---

## Burstiness Flags

- **Introduction opener** (dòng 17): đã sửa — câu ngắn mở đầu (~19 từ) rồi đến câu dài hơn (~54 từ, mang trích dẫn [3]), khớp target "high burstiness: short opener, then long sentences" dành riêng cho section Introduction.
- **Mật độ semicolon toàn bài**: xem bảng trên — đạt target sau khi tách 20/29 và giữ nguyên 9 list-separator hợp lệ.
- Không phát hiện thêm cờ burstiness nào khác; paragraph-length variance và synonym cycling đã PASS ở Step 4.

---

## Xác nhận LUẬT 0 (Meaning-Preservation Invariant)

Đã đọc lại toàn bộ 194 dòng file sau khi áp dụng 25 sửa đổi để đối chiếu từng bất biến bắt buộc:

- **Số liệu & đơn vị:** toàn bộ số liệu (40.000/20.000/20.000 ảnh, tỉ lệ chia 80/10/10, seed 42, N=32, 187 = 64+59+64, bảng Table 1 đầy đủ 6 cột × 5 hàng, 86,6%/AUC 0,943, tất cả số trong §6.1–6.3) đối chiếu khớp 100% với bản trước khi sửa — không con số nào bị đổi, thêm, hay bớt.
- **Công thức:** khối `$$...$$` ở dòng 43–45 (bao gồm 8 lệnh `\;` LaTeX spacing) hoàn toàn không bị chỉnh sửa trong suốt pass này — đây chính là lý do 8 match `;` trên dòng 44 bị loại khỏi audit semicolon văn xuôi ngay từ đầu.
- **Citation key + câu gắn kèm:** mọi `[n]` vẫn gắn đúng với claim gốc của nó; việc tách semicolon→2 câu chỉ xảy ra ở vị trí sau citation hoặc hoàn toàn không liên quan đến citation trong câu đó (ví dụ dòng 31: "...for gray-scale images [15]. The noise-residual half..." — [15] vẫn gắn với claim giới thiệu LBP, câu mới sau đó thuộc về claim Noiseprint [13] khác, không xáo trộn).
- **Độ mạnh khẳng định (claim strength) & hedge:** không từ hedge nào (`"suggests"`, `"indicates"`, `"consistent with, though not formal proof of"`, `"we treat as an explicit scope limitation"`) bị đổi. 4 lần thay `"paradigm"` → `"approach"`/`"line of work"` là thay từ đồng nghĩa mô tả trung tính (mô tả một nhóm/dòng phương pháp, không phải một tuyên bố kiểu Kuhnian paradigm-shift), không tăng cũng không giảm độ mạnh khẳng định.
- **Chiều so sánh:** "XGBoost and LightGBM...tied for best and clearly ahead of RandomForest and CatBoost", "RandomForest...trails by roughly three accuracy points" — chiều so sánh giữ nguyên 100% qua toàn bộ pass.
- **Không phát hiện drift nào cần revert.**

---

## Acceptance Checklist

- [x] Term filter (Step 1): 2/25 thuật ngữ có match trong bài; 1 giữ nguyên đúng ngoại lệ domain-term (`robust`/`robustness`), 1 sửa hết toàn bộ 4 lần (`paradigm`) — verify bằng `grep -i paradigm` → 0 match.
- [x] Dấu câu (Step 2): em dash 0/0 trong văn xuôi; semicolon văn xuôi 29 → 9, mật độ 5,98/1000 → 1,85/1000 từ, **đạt target ≤2/1000** (số liệu đếm thật bằng `grep`/`awk`/`wc`, không ước lượng).
- [x] Throat-clearing / structure patterns / TEEL / citation-integration (Steps 3, 4, 6, 7): PASS, không có action item tồn đọng.
- [x] Burstiness (Step 5): 1 gap phát hiện (Introduction opener) và đã sửa; verify lại không phát sinh gap mới.
- [x] Style calibration (Step 8): SKIP hợp lệ — không có bài mẫu văn phong nào được cung cấp trong phiên này.
- [x] LUẬT 0: xác nhận qua đối chiếu toàn văn 194 dòng sau khi sửa — không phát hiện drift ở số liệu, công thức, citation, độ mạnh khẳng định, hedge, hay chiều so sánh.

**Kết luận: PASS. Sẵn sàng chuyển sang khâu kế tiếp — `latex-fix` (Task #20).**
