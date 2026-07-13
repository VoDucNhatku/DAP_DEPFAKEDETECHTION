# Claims Ledger — DAP_DEPFAKEDETECHTION / Research-Deepfake

Append-only. Một dòng cho mỗi claim novelty/venue. Không sửa dòng cũ — revision tạo dòng mới, đánh dấu dòng cũ `revised→C-n`.

| id | date | proposal | tier | venue band + điều kiện | status | artifact |
|---|---|---|---|---|---|---|
| C-1 | 2026-07-09 | Mở rộng pipeline classification-trên-PCA-residual bằng: (a) sweep đa mức N + tương quan với đường KS-divergence gốc của Xie et al. (arXiv:2604.17268), (b) sửa bug LBP (`uniform`/`nri_uniform`), (c) chạy ablation-với-classifier, (d) Related Work thật (8 nguồn verify), (e) robustness test cơ bản | T1 | Workshop / hội nghị Q4 / Scopus-index — **không phải Q1, không phải Q2-Q3 một mình**. Lên band cao hơn cần (T2) module kiến trúc mới thật sự (ví dụ: lacunarity làm learnable pooling layer per arXiv:2404.16268 — chưa làm, ngoài phạm vi Q4 lần này) | active | `notes/synthesize-gaps-deepfake-pca-residual.md` |
| C-2 | 2026-07-13 | **Phạm vi thực tế của bản thảo Q4 soạn lần này** (con của C-1, không phải claim mới): CHỈ trình bày làm contribution đã hoàn thành — (b) LBP `nri_uniform` đúng về toán học [P(P−1)+3=59, verify qua code], pipeline 187-chiều (FFT 64 + LBP 59 + Noise-residual 64) trên PCA-residual N=32 (N kế thừa từ default của S1/Xie et al., không phải sweep nội bộ), 5 classifier đã chạy thật 2 lần độc lập (LightGBM Test Acc 0.8662/F1 0.8664/AUC 0.9427), và (d) Related Work 15 nguồn verify (S1–S8 + [9]–[14] + Ojala et al. 2002). Mục (a) sweep-N/tương quan KS, (c) ablation-với-classifier (PCA-residual vs raw), (e) robustness test — **chưa có kết quả thật, đưa vào bài dưới dạng Limitations/Future Work, không claim là contribution đã xong**. Không có SOTA deep-learning baseline nào được fine-tune trên đúng split này — số liệu literature (S3/S4/[9]) chỉ trích dẫn làm ngữ cảnh, không phải so sánh kiểm soát trực tiếp. | T1 | Workshop / hội nghị Q4 / Scopus-index — giữ nguyên band của C-1, không tự nâng | active | `paper/` |

---

## Ghi chú áp dụng

- **Trước khi trả lời bất kỳ câu hỏi follow-up nào** về novelty/venue của dự án này: đọc lại dòng C-1 + `notes/synthesize-gaps-deepfake-pca-residual.md` — không trả lời từ trí nhớ hội thoại (research-proposal-integrity.md §3).
- **Downgrade trigger cho C-1:** nếu sweep N (mục "White space" trong file gaps) cho kết quả tương quan yếu/không ý nghĩa thống kê giữa accuracy-vs-N và KS-stat-vs-N, phần "cầu nối thực nghiệm" trong bài phải viết lại thành "quan sát sơ bộ" thay vì "chứng minh liên hệ" — cần append dòng revision mới nếu điều này xảy ra sau khi chạy thực nghiệm.
- **Không có claim Q1 nào được đưa ra trong dự án này** — không cần dòng ledger nào khác ngoài C-1 tại thời điểm hiện tại.
