# LaTeX Fix Report — main.md

**File:** `D:\CPV-VIP\paper\main.md` (194 dòng)
**Khâu:** `latex-fix` — Task #20, bước 4/6 trong pipeline `paper-writing-integrity.md` §6
**Khâu trước:** `style-humanizer` — PASS (xem `paper/reports/style-humanizer.md`)
**Ngày:** 2026-07-14

---

## Quy trình

Chạy linter bundled (script-offloading, không quét bằng mắt):
```
python latex-fix/scripts/latex_lint.py D:/CPV-VIP/paper/main.md
```
Kết quả thô: `{"findings": 1, "files_flagged": ["main.md"], "files_scanned": 1}`.

## Fix-log

| File | Dòng | Rule | Severity | Match | Xử lý |
|---|---|---|---|---|---|
| main.md | 45 | `display-no-blank-before` | warn | `$$` | **False positive đã verify — KHÔNG sửa** (xem giải thích bên dưới) |

## Giải thích false positive

Hàm `_has_unspaced_display()` của linter kiểm tra "dòng liền trước có blank không" cho **mọi** dòng chỉ chứa `$$`, mà không phân biệt đây là delimiter MỞ hay ĐÓNG của khối. Khối công thức duy nhất trong file (đọc trực tiếp dòng 42–46):

```
42: (blank)
43: $$
44: R_i \;=\; \mu \;+\; \sum_{k=33}^{256} c_{i,k}\, u_k \;=\; I_i \;-\; \sum_{k=1}^{32} c_{i,k}\, u_k
45: $$
46: (blank)
```

Dòng 43 (mở) có dòng 42 blank trước nó → đúng chuẩn, linter không flag. Dòng 45 (đóng) có dòng 44 — chính là **nội dung công thức** — trước nó, và đó là cấu trúc hoàn toàn đúng của một khối `$$...$$` (nội dung nằm giữa hai delimiter, không chèn dòng trắng ở giữa). Linter áp nhầm rule "cần blank line trước" — vốn chỉ đúng cho delimiter mở — sang cả delimiter đóng.

Đối chiếu `latex-katex-compat.md`: yêu cầu nguyên văn là blank line **before and after the block** (bao quanh cả khối), không phải bên trong khối. File hiện tại đã thỏa đúng cả hai điều kiện đó (dòng 42 trước khối, dòng 46 sau khối). Nếu áp "fix" cơ học — chèn thêm một dòng trắng giữa dòng 44 và 45 — sẽ vi phạm chính rule này (chèn blank line vào GIỮA khối thay vì quanh khối) và có rủi ro khiến một số cấu hình markdown-it/KaTeX hiểu nhầm thành hai khối tách rời. **Quyết định: giữ nguyên nội dung, không sửa.**

Verify bổ sung: `grep '\$\$' main.md` trên toàn file → đúng một cặp `$$` (dòng 43 và 45), không có `$$` nào khác trong 194 dòng → không có finding nào bị bỏ sót do bug đếm parity của linter.

## Các rule khác — 0 finding (verify bằng chính linter, quét toàn file 194 dòng)

| Rule | Mục tiêu | Kết quả |
|---|---|---|
| `tag-macro`, `label-ref-macro` | Yêu cầu bổ sung của người dùng: không hyperlink xanh cho công thức (`\tag`/`\label`/`\ref`/`\eqref`) | 0 match |
| `bracket-display-delim`, `paren-inline-delim`, `fenced-math-block` | Delimiter sai chuẩn (`\[...\]`, `\(...\)`, ```` ```math ````) | 0 match |
| `boldsymbol-macro`, `operatorname-macro`, `middle-bar` | Macro KaTeX-fragile | 0 match |
| `plaintext-subscript/norm/argminmax/greek` | Toán viết ASCII thô (`L_total`, `||x||`, `theta`, `argmin`) ngoài vùng math thật | 0 match |

## Bước compile

Bản thảo là Markdown thuần (`paper/main.md`), không phải file `.tex` — không có bước build PDF qua `pdflatex`/`xelatex` trong pipeline này. Đúng theo premise của `latex-katex-compat.md`: mục tiêu là công thức render đúng trên **VS Code Markdown preview (KaTeX)** và **GitHub (MathJax)** trực tiếp từ `.md`, không phải một pipeline LaTeX biên dịch ra PDF. Không claim "đã compile" vì bước đó không áp dụng cho định dạng hiện tại của bản thảo.

## Kết luận

**PASS.** 0 sửa đổi thực sự cần thiết trên nội dung; 1 cảnh báo linter được verify là false positive (bug parity mở/đóng của `_has_unspaced_display()`) và được ghi nhận kèm lý do thay vì áp dụng máy móc. Công thức duy nhất trong bài (dòng 43–45, phương trình ảnh dư PCA) giữ nguyên 100% — khớp với xác nhận LUẬT 0 của `style-humanizer` ở khâu trước. Sẵn sàng chuyển sang khâu kế tiếp — `ieee-q1-devil-advocate` (Task #21).
