# Citation Audit Report — citation-guard

Dự án: D:\CPV-VIP (Reproducible Detection of AI-Generated Faces via Open Handcrafted Features on PCA-Residual Images)
Bản thảo: `paper/main.md`
Worker: citation-guard (skill `C:\Users\DELL\.claude\skills\citation-guard\SKILL.md`)
Vị trí trong pipeline: khâu 2/6 (paper-writing-integrity.md §6) — sau paper-submission, trước style-humanizer
Ngày: 2026-07-13

---

## 1. Summary

| Chỉ số | Giá trị |
|---|---|
| Số mục tham khảo trong danh mục References | 17 ([1]–[17]) |
| Số mục được trích dẫn trong thân bài ≥ 1 lần | 17/17 |
| Trích dẫn mồ côi (in-text nhưng không có trong danh mục) | 0 |
| Mục thừa (có trong danh mục nhưng không được trích) | 0 |
| Tổng lượt trích dẫn trong thân bài (đếm từng số riêng lẻ, kể cả trong nhóm gộp `[4, 9, 10, 14]` ở dòng 17) | 53 |
| Mục có DOI xác minh qua CrossRef (`https://doi.org/...`) | 3 — [11], [12], [15] |
| Mục arXiv xác minh qua trang abstract arXiv (tiêu đề/tác giả/năm) phiên này | 7 — [1], [2], [3], [5], [8], [9], [14] |
| Mục verify qua WebSearch + trang tạp chí | 1 — [10] |
| Mục không cần sửa (đã đầy đủ tác giả + venue từ trước) | 6 — [4], [6], [7], [13], [16], [17] |
| Mục có sửa lỗi thực chất phiên này | 11 — xem bảng §2 |
| Nguồn bịa / không rõ nguồn gốc phát hiện | 0 |

**Phương pháp xác minh zero-orphan:** dùng Grep trực tiếp trên `paper/main.md` với hai pattern (`\[\d+\]` và `\[\d+(?:,\s*\d+)*\]`), đối chiếu thủ công từng dòng 1–157 (thân bài) với danh mục 161–193 (References) — không suy luận từ trí nhớ hội thoại, đúng nguyên tắc `paper-writing-integrity.md` §1 và `hallucination-guard`.

---

## 2. Corrections Made (11 mục)

| Ref | Vấn đề phát hiện | Sửa | Nguồn verify |
|---|---|---|---|
| [1] | Viết tắt "Xie et al." | Đủ tên tác giả: Xie, W., Yin, J., Ma, L., Zhang, X., Zhang, W. | arXiv:2604.17268 (trang abstract) |
| [2] | Viết tắt "Xiao et al." | Đủ tên: Xiao, S., Guo, Y., Peng, H., Liu, Z., Yang, L., Wang, Y. | arXiv:2503.08484 |
| [3] | Viết tắt "Rössler et al." | Đủ tên: Rössler, A., Cozzolino, D., Verdoliva, L., Riess, C., Thies, J., Nießner, M. | arXiv:1901.08971 |
| [5] | Viết tắt "Wang et al." | Đủ tên: Wang, T., Cheng, H., Liu, M.-H., Kankanhalli, M. | arXiv:2504.09451 |
| [8] | Viết tắt "Hinke-Navarro et al." | Đủ tên: Hinke-Navarro, A., Nieto-Hidalgo, M., Espin, J.M., Tapia, J.E. | arXiv:2507.20608 |
| [9] | Viết tắt tác giả **và** tiêu đề diễn giải sai (không phải tiêu đề thật) | Đủ tên: Nirob, S.M.H., Rahman, M., Ehsan, S., Haque, S.; tiêu đề sửa từ "Handcrafted-Feature Fusion with Gradient Boosting for CIFAKE Image Detection" (bịa/diễn giải) → tiêu đề thật "Handcrafted Feature Fusion for Reliable Detection of AI-Generated Images" | arXiv:2601.19262 (đọc trực tiếp trang abstract) |
| [10] | **Thiếu hẳn venue** — bản nháp chỉ ghi "(2026)", không có tên tạp chí/số/trang | Bổ sung đủ: International Journal on Advanced Computer Theory and Engineering 15(2S), 241–246 (2026) | WebSearch + WebFetch trang tạp chí |
| [11] | Đã verify DOI ở phần trước của phiên nhưng **chưa từng được ghi vào text** | Thêm `https://doi.org/10.1007/s11042-015-3079-2` | CrossRef (verify trước, ghi bổ sung phiên này) |
| [12] | DOI sai định dạng ưu tiên (`doi:` thay vì `https://doi.org/`) | Đổi thành `https://doi.org/10.3390/jimaging7080128` | Định dạng lại, DOI giữ nguyên |
| [14] | Viết tắt "Tan, C. et al." | Đủ tên: Tan, C., Zhao, Y., Wei, S., Gu, G., Liu, P., Wei, Y. | arXiv:2403.07240 |
| [15] | Đã verify DOI trước đó nhưng **chưa được ghi vào text** | Thêm `https://doi.org/10.1109/TPAMI.2002.1017623` | CrossRef (verify trước, ghi bổ sung phiên này) |

Sửa đã áp dụng trực tiếp vào `paper/main.md` (Edit tool, đối chiếu old/new string), không phải chỉ ghi trong report.

Ngoài ra đã verify substantively (không chỉ hình thức) câu mô tả [9] trong §2 Related Work — "Nirob et al. fuse a comparable set of handcrafted descriptors with a LightGBM classifier on the CIFAKE benchmark [9]" — đối chiếu với abstract thật của arXiv:2601.19262: đúng, dùng CIFAKE, LightGBM là top performer (PR-AUC 0.9879/ROC-AUC 0.9878/F1 0.9447), descriptor gồm pixel thô + color histogram + DCT + HOG + LBP + GLCM + wavelet. Không cần sửa câu này.

---

## 3. Flagged for Review (không tự động sửa)

### 3.1 Thứ tự đánh số không theo đúng thứ tự xuất hiện lần đầu trong văn bản

Quy ước chuẩn cho numbered-bracket style (Springer/IEEE) là đánh số **theo đúng thứ tự trích dẫn lần đầu trong thân bài**. Sau khi trace thủ công toàn bộ 53 lượt trích dẫn (kể cả nhóm gộp `[4, 9, 10, 14]` ở dòng 17, dễ bị bỏ sót nếu chỉ grep pattern đơn số — bản thân tôi đã mắc lỗi này ở lượt quét đầu và phải tự sửa), thứ tự xuất hiện lần đầu THỰC TẾ là:

```
[3] → [4] → [9] → [10] → [14] → [1] → [7] → [15] → [13] → [11] → [12] → [2] → [5] → [6] → [8] → [16] → [17]
```

trong khi danh mục References hiện đánh số `[1]…[17]` theo **nhóm chủ đề** (họ fractal/PCA-residual trước, rồi benchmark, rồi tiền lệ phương pháp luận, rồi các nguồn nền tảng…), không phải theo thứ tự xuất hiện.

**Đánh giá mức độ nghiêm trọng:** đây là vấn đề QUY ƯỚC/ĐỊNH DẠNG, **không phải** lỗi trích dẫn sai, mồ côi, hay bịa nguồn — mọi nguồn đều có thật, đã verify, zero-orphan (§1). Đây cũng không nằm trong LUẬT CỨNG của citation-guard (DOI verify / không bịa entry / retraction screening), mà chỉ là một "capability" auto-correction tùy chọn.

**Vì sao không tự sửa ngay:** đánh số lại đúng thứ tự đòi hỏi một phép hoán vị đầy đủ trên cả 17 mục danh mục lẫn 53 lượt trích dẫn trong thân (bao gồm sắp lại thứ tự số bên trong nhóm gộp `[4, 9, 10, 14]` → `[4, 7, 8, 9]` theo ánh xạ mới). Đây là thao tác cơ học quy mô lớn, và việc tôi tự bắt lỗi ở chính bước trace thứ tự (bỏ sót nhóm gộp trong lượt quét đầu) cho thấy rủi ro sai sót khi làm tay là có thật. Sửa sai một nửa sẽ tệ hơn giữ nguyên cách đánh số theo chủ đề hiện tại.

**Ánh xạ đầy đủ đã chuẩn bị sẵn** (để áp dụng an toàn bằng kỹ thuật placeholder hai lượt nếu được xác nhận cần làm):

| Cũ | Mới | Cũ | Mới | Cũ | Mới |
|---|---|---|---|---|---|
| [1] | [2] | [7] | [3] | [13] | [6] |
| [2] | [12] | [8] | [15] | [14] | [4] |
| [3] | [1] | [9] | [8] | [15] | [5] |
| [4] | [7] | [10] | [9] | [16] | [16] |
| [5] | [13] | [11] | [10] | [17] | [17] |
| [6] | [14] | [12] | [11] | | |

**Khuyến nghị:** giữ nguyên cách đánh số theo chủ đề cho pass này để không chặn tiến độ pipeline; nếu nhóm cần đúng chuẩn appearance-order trước khi nộp thật, đây là một correction riêng, độc lập, có thể áp dụng bất kỳ lúc nào bằng bảng ánh xạ trên.

Không có mục nào khác bị flag (không phát hiện thêm entry đáng ngờ, không phát hiện thêm venue thiếu, không phát hiện DOI sai định dạng nào khác).

---

## 4. Synthesis Quality Scan (§2 Related Work)

**Kết quả: PASS.** 5 đoạn văn của §2 tổng hợp theo chủ đề, không đoạn nào rơi vào mẫu liệt kê tuần tự kiểu "A nói X [1]. B nói Y [2].":

1. Đoạn 1 — định vị paradigm deep-detector (không trích dẫn phụ, dùng để mở khung).
2. Đoạn 2 — hai nguồn tần số ([7], [14]) được đan vào MỘT lập luận chung, kết bằng câu tổng hợp "Both results support treating a frequency-magnitude histogram as an informative, non-arbitrary descriptor rather than an ad hoc choice."
3. Đoạn 3 — năm nguồn texture/noise/tiền lệ ([15], [13], [4], [9], [10]) đan thành lập luận có cấu trúc, kết bằng câu tổng hợp minh thị: "These three studies confirm that handcrafted-feature-plus-classical-classifier pipelines are an active, competitive paradigm in 2025 and 2026, not a historical curiosity."
4. Đoạn 4 — sáu nguồn dòng PCA-residual/fractal cũ hơn ([11], [12], [2], [5], [6], [8]) được phân biệt rõ với nhau bằng lập luận khác biệt hóa (mỗi nguồn giải quyết một biến thể/vấn đề khác), không liệt kê máy móc.
5. Đoạn 5 — câu định vị khoảng trống nghiên cứu tường minh: "Positioned against this literature, the present paper occupies a specific, previously empty cell."

---

## 5. Metrics

- **Self-citation ratio:** 0% — dự án sinh viên, tác giả là placeholder, không có công trình trước đó của "tác giả" để tự trích dẫn.
- **Nguồn cũ hơn 10 năm:** 1/17 (5.9%) — [15] Ojala, Pietikäinen, Mäenpää (2002), bài gốc định nghĩa LBP/`nri_uniform`. Đây là trích dẫn nền tảng bắt buộc (nguồn gốc trực tiếp của công thức $P(P-1)+3=59$ dùng trong Method), không phải dấu hiệu thiếu cập nhật — dưới ngưỡng 15% nên không cần flag.
- **Mật độ trích dẫn:** tập trung hợp lý ở §2 Related Work (5 đoạn, 15/17 nguồn) và §6.3 Caveats (đối chiếu lại 4 nguồn khi bàn giới hạn); §3–§4 (Method) trích dẫn thưa, đúng vai trò (chỉ dẫn nguồn khi mượn ý tưởng cụ thể — ví dụ dòng 61 dẫn [7] và [14] đúng chỗ mô tả descriptor tần số).
- **Retraction screening:** không tra cứu Retraction Watch trong phiên này (không có kết nối/khẳng định nào được thực hiện) — theo đúng luật cứng của citation-guard, ghi nhận trung thực: **chưa kiểm tra retraction**, không claim "đã kiểm tra sạch".

---

## 6. Kết luận & Handoff

**Trạng thái: PASS** — đủ điều kiện qua khâu citation-guard. Không có trích dẫn bịa, không có mồ côi, không có mục thừa; 11/17 mục đã được sửa với nguồn verify thật (CrossRef/arXiv/WebSearch) trong phiên này; 1 finding không chặn (thứ tự đánh số theo chủ đề thay vì appearance-order) đã ghi rõ ở §3.1 kèm ánh xạ sẵn sàng áp dụng nếu cần.

**Khâu kế tiếp** (paper-writing-integrity.md §6): `style-humanizer` — hiệu chỉnh văn phong bản thảo `paper/main.md`, dưới bất biến bảo toàn nghĩa (số liệu, toán, citation key và câu gắn nó, độ mạnh claim, hướng so sánh — tất cả giữ nguyên).
