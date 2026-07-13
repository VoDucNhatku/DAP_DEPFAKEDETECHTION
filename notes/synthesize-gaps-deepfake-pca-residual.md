# Gaps Synthesis — PCA-Residual Handcrafted-Feature Classification cho AI-Generated Face Detection

- **Scope:** 8 bài báo verify qua web (arXiv, không có `papers/` local) + 1 dự án sinh viên đang triển khai (`D:\CPV-VIP\DAP_DEPFAKEDETECHTION`)
- **Worker:** paper-synthesize (mode `gaps`, N=8 → tier Overview theo workbench-conventions §7)
- **Date:** 2026-07-09
- **Nguồn tham chiếu song song:** `notes/deepfake-action-plan.md`, `notes/deepfake-status-report.md`

---

## 1. Danh sách nguồn (đã verify thật, không bịa)

| id | Trích dẫn | Verify qua | Venue/status |
|---|---|---|---|
| S1 | Xie, W., Yin, J., Ma, L., Zhang, X., Zhang, W. (2026). *Fractal Characterization of Low-Correlation Signals in AI-Generated Image Detection.* arXiv:2604.17268 | WebFetch arXiv abs + đọc trực tiếp `Research-Deepfake/src/{feature.py,common.py,extract_feature.py,paper.ipynb,main.ipynb}` | Preprint (nộp 19/04/2026), chưa rõ venue đích |
| S2 | Xiao, S., Guo, Y., Peng, H., Liu, Z., Yang, L., Wang, Y. (2025). *Generalizable AI-Generated Image Detection Based on Fractal Self-Similarity in the Spectrum.* arXiv:2503.08484 | WebFetch arXiv abs | Preprint, cs.CV, chưa qua peer review |
| S3 | Rössler, A., Cozzolino, D., Verdoliva, L., Riess, C., Thies, J., Nießner, M. (2019). *FaceForensics++: Learning to Detect Manipulated Facial Images.* arXiv:1901.08971 | WebSearch + WebFetch | **ICCV 2019** (đã publish, canonical benchmark) |
| S4 | Yasir, S.M., Kim, H. (2025). *Lightweight Deepfake Detection Based on Multi-Feature Fusion.* arXiv:2502.11763 | WebFetch arXiv abs | **Applied Sciences 2025, 15(4):1954** (đã publish, MDPI) |
| S5 | Wang, T., Cheng, H., Liu, M.-H., Kankanhalli, M. (2025). *FractalForensics: Proactive Deepfake Detection and Localization via Fractal Watermarks.* arXiv:2504.09451 | WebFetch arXiv abs | **ACM Multimedia 2025 (Oral)** |
| S6 | Mohan, A., Peeples, J. (2024). *Lacunarity Pooling Layers for Plant Image Classification using Texture Analysis.* arXiv:2404.16268 | WebFetch arXiv abs | CVPR 2024 Workshop (Vision for Agriculture) |
| S7 | Zhang, X., Karaman, S., Chang, S.-F. (2019). *Detecting and Simulating Artifacts in GAN Fake Images.* arXiv:1907.06515 | WebFetch arXiv abs | WIFS 2019 |
| S8 | Hinke-Navarro, A., Nieto-Hidalgo, M., Espin, J.M., Tapia, J.E. (2025). *Enhanced Deep Learning DeepFake Detection Integrating Handcrafted Features.* arXiv:2507.20608 | WebFetch arXiv abs | Preprint, cs.CV |

**S0 (dự án đang đánh giá):** Nhóm sinh viên — thay thế toolkit đóng FreeAeon (S1) bằng đặc trưng thủ công mở (FFT-histogram 64-bin + LBP-histogram 59-bin + noise-residual-histogram 64-bin = vector 187-chiều) trên ảnh PCA-residual (N=32 cố định), huấn luyện 5 classifier cổ điển. Kết quả verify thật: LightGBM Test Acc **86.6%**, AUC **0.94** (chọn model qua validation set, không nhìn test set trước — đúng thực hành).

---

## 2. Giới hạn từng nguồn (quan sát trực tiếp, có dẫn id)

- **S1** — Chỉ chạy KS-test thống kê (khác biệt phân phối) giữa real/fake theo từng PCA-level; **chưa từng chứng minh tín hiệu đó có phân biệt được (classification) hay không** — statistical significance ≠ classification utility, đây là khoảng trống lớn nhất S1 để lại. Toolkit trích đặc trưng (FreeAeonFractal/FreeAeonML) đóng nguồn — không ai ngoài tác giả tái lập được FD/MFS/Lacunarity. PCA fit **theo từng ảnh riêng lẻ** (không phải basis chung) — S1 không bàn liệu điều này có ảnh hưởng tính hợp lệ của KS-test gộp hàng nghìn ảnh hay không.
- **S2** — Cơ chế khác hẳn (fractal self-similarity trong phổ tần số toàn ảnh, không qua PCA-residual); preprint, chưa peer-review; không kiểm tra tương tác giữa self-similarity phổ và phép biến đổi PCA-residual.
- **S3** — Benchmark 2019, tập trung manipulation cục bộ (DeepFakes/Face2Face/FaceSwap/NeuralTextures) — **khác miền** với full-face GAN synthesis (StyleGAN/`1-million-fake-faces`) mà S0 dùng; số Xception của S3 **không thể so trực tiếp** với accuracy của S0 nếu không tự chạy lại trên đúng dữ liệu S0.
- **S4** — Đặc trưng thủ công (HOG+LBP+KAZE) + 4 classifier cổ điển đạt 92%/96% — **nhưng trên ảnh gốc, không qua bất kỳ phép biến đổi residual/tần số nào**; không kiểm tra liệu tiền xử lý dạng residual (như PCA-residual của S0) có giúp ích hay có hại cho khả năng phân biệt của đặc trưng thủ công.
- **S5** — Proactive (nhúng watermark trước khi bị chỉnh sửa) — khác mô hình đe dọa hoàn toàn với passive detection của S0; chỉ có giá trị ngữ cảnh (chứng minh "fractal" là từ khóa nóng ở venue top-tier 2025), không phải đối thủ phương pháp trực tiếp.
- **S6** — Miền hoàn toàn khác (phân loại ảnh thực vật); lacunarity mới chỉ được thử làm pooling layer khả vi trong CNN — **chưa ai thử lacunarity/fractal pooling cho bài toán AI-image detection** — đây là white space thật nhưng ngoài phạm vi implementation hiện tại của S0 (S0 dùng FFT/LBP/noise, không dùng lacunarity).
- **S7** — 2019, thời CycleGAN — kiến trúc GAN đã tiến hóa nhiều (StyleGAN2/3, diffusion); tín hiệu artifact do upsampling có thể đã yếu đi với generator mới — cần nêu như một caveat khi S0 dùng FFT-histogram làm cơ sở lý luận.
- **S8** — Xu hướng field giữa 2025 đã chuyển sang **hybrid** (đặc trưng thủ công + CNN sâu fusion), không còn dừng ở "chỉ đặc trưng thủ công + ML cổ điển" — đây là rủi ro review: cách tiếp cận thuần-ML-cổ-điển của S0 (không có nhánh CNN nào) có thể bị đánh giá là "đi sau" so với chuẩn 2025-2026 nếu không có điểm khác biệt rõ.

---

## 3. Khoảng trống liên-nguồn (cross-cutting gaps)

| # | Gap | Bằng chứng (id) |
|---|---|---|
| G1 | **KS-test ý nghĩa thống kê ≠ khả năng phân loại thực tế** — chưa nguồn nào (kể cả S1) đóng vòng lặp này cho khung fractal/PCA-residual của S1 | S1 |
| G2 | **Không nguồn nào kiểm tra độ nhạy accuracy-vs-N** (N = số component PCA bị loại) — S1 quét N=1-129 chỉ cho KS-test, S0 cố định N=32 không có justification độ nhạy | S1, S0 |
| G3 | **Đặc trưng thủ công "thuần cổ điển ML" (không CNN) đã là paradigm cũ (đầu 2025)** — S4 đã công bố y hệt pattern "handcrafted+classical-ML" (Applied Sciences 2025); field đang chuyển sang hybrid CNN+handcrafted (S8, giữa 2025) | S4, S8 |
| G4 | **Không kiểm tra generalization cross-generator** (StyleGAN vs diffusion vs GAN khác) — đúng vấn đề mà S2 nêu là khó | S2, S0 |
| G5 | **Chưa test robustness** dưới nén JPEG / resize / blur / noise — kỳ vọng chuẩn từ 2019 (S3) mà S0 chưa chạm | S3, S0 (đã ghi nhận trong action-plan P1) |
| G6 | **Lỗi nội bộ tái lập (không phải gap literature)**: LBP method không nhất quán giữa 2 notebook (`'uniform'` vs `'nri_uniform'`) — rủi ro tính toàn vẹn nếu không sửa trước khi nộp | quan sát trực tiếp code S0 |

## 4. White space — chưa ai làm (cơ hội thật)

**Cầu nối thực nghiệm cụ thể, chưa từng được làm bởi bất kỳ nguồn nào ở trên:**
*"Liệu accuracy phân loại trên đặc trưng thủ công PCA-residual (mở, tái lập được) có theo cùng xu hướng với đường cong phân kỳ KS-test mà S1 báo cáo qua các mức PCA-level hay không?"*

**Verify tính khả thi (quan trọng — không phải suy đoán):**
- File `Research-Deepfake/data/face/stats/train/common.csv` (18,200 dòng, đủ pca level 0-129, cả real/fake, các thống kê entropy/mean/std/skew/kurt) **đã có sẵn local**, đây chính là `df_stats` mà `paper.ipynb` cell 11 nạp vào.
- Hàm `normality_check`/`distribution_similarity_check` (định nghĩa trong `paper.ipynb` cell 2) **chỉ dùng `scipy.stats.kstest`** — hoàn toàn mở, không phụ thuộc FreeAeon.
- ⟹ Nhóm sinh viên **có thể tái lập chính xác đường cong KS-divergence-vs-PCA-level của S1** (cho nhóm "common" stats: fd/entropy/mean/skew/kurt/std) mà không cần toolkit đóng nguồn, dùng dữ liệu đã có trong repo.
- Việc còn lại: chạy pipeline classifier hiện có của S0 (chỉ cần lặp qua nhiều mức N thay vì cố định N=32 — code đã có sẵn hàm `get_pca_residual_image(num_components_to_remove=N)`) rồi vẽ accuracy-vs-N cạnh KS-stat-vs-N của S1 → tính hệ số tương quan (Pearson/Spearman).
- Chi phí: rẻ (không cần thu thập dữ liệu mới, không cần FreeAeon, chỉ cần re-run pipeline đã có ở ~6-8 mức N).

*Lưu ý phạm vi: verify chỉ xác nhận tính khả thi cho nhóm đặc trưng "common" (fd/entropy/mean/skew/kurt/std). File `mfs_similar.csv`/`lac_*.csv` (KS-test cho MFS/Lacunarity) **không có sẵn local** — nếu muốn mở rộng cầu nối này sang MFS/Lacunarity, nhóm cần liên hệ tác giả S1 xin thêm dữ liệu hoặc giới hạn tuyên bố ở phạm vi "fd" mà thôi.*

---

## 5. Bảng cơ hội (gap → vì sao quan trọng → hướng cụ thể → nguồn → tier + venue band)

| Gap | Vì sao quan trọng | Hướng cụ thể | Nguồn | Tier | Venue band |
|---|---|---|---|---|---|
| G1+White space | Đóng vòng lặp "ý nghĩa thống kê → khả năng phân loại" — đây là **đóng góp thực nghiệm mới, xác thực khả thi bằng dữ liệu đã có** | Sweep N ∈ {8,16,24,32,40,48,64,96,128}, chạy lại pipeline classifier hiện có của S0 ở mỗi N, so sánh accuracy-vs-N với KS-stat-vs-N tái lập từ `common.csv` | S1, S0 | **T1** (mở rộng thực nghiệm, không đổi kiến trúc) | Q4 conference / hội nghị Scopus-index — **đủ điều kiện nếu chạy xong + báo cáo trung thực** |
| G2 | S0 cố định N=32 không có cơ sở; reviewer Q4 sẽ hỏi "tại sao 32" | Cùng 1 lần chạy sweep trên → chọn N tối ưu theo accuracy, so với N=32 mặc định của S1's Section 6 | S1, S0 | T1 | Q4 / Scopus |
| G3 | Reviewer 2025-2026 có thể chê "chỉ ML cổ điển là cũ" | KHÔNG bắt buộc thêm CNN (tốn thời gian, rủi ro) — thay vào đó **định vị rõ trong bài**: đóng góp không phải "beat SOTA accuracy" mà là "cầu nối thực nghiệm KS→classification cho khung fractal của S1", né được so sánh trực diện với S4/S8 | S4, S8 | — (định vị, không phải hướng mới) | — |
| G4 | Generalization cross-generator là câu hỏi khó, S2 chưa trả lời | **Không đưa vào Q4 lần này** (out of scope, cần thêm dataset) — ghi rõ "Limitation/Future Work", tránh overclaim | S2 | — | Not runnable as stated cho vòng nộp này |
| G5 | Kỳ vọng chuẩn từ 2019 (S3), thiếu sẽ bị soi | Chạy robustness test đã có trong plan P1 (JPEG q=50, resize 50%, blur σ=2, noise N(0,10)) — dùng ảnh test set sẵn có, biến đổi rồi re-infer bằng model đã train, không cần train lại | S3, S0 | T1 | Q4 / Scopus |
| G6 | Bug tái lập nội bộ — không sửa thì mọi con số ablation sau này (nếu dùng LBP) đều đáng ngờ | Chuẩn hoá 1 trong 2: `nri_uniform` + 59 bin (khớp toán học, khuyến nghị) HOẶC `uniform` + đúng 10 bin (không phải 59) — xem §6 bên dưới | quan sát code | — (data-integrity fix, không phải hướng nghiên cứu) | — |

---

## Venue Claim Card

- **Proposal:** Mở rộng pipeline classification-trên-PCA-residual hiện có của nhóm bằng (a) sweep đa mức N + tương quan với đường KS-divergence gốc của S1 (đóng góp thực nghiệm mới), (b) sửa bug LBP, (c) chạy ablation-với-classifier trên `train_ablation.pkl` đã build sẵn, (d) Related Work thật (8 nguồn trên), (e) robustness test cơ bản
- **Novelty tier:** **T1 — recipe/thực nghiệm mở rộng.** Không đổi kiến trúc, không tái định nghĩa bài toán. Thay công cụ đóng nguồn (FreeAeon) bằng đặc trưng mở + thêm classification + thêm cầu nối thực nghiệm với KS-test gốc. Xem §1 rubric `research-proposal-integrity.md`: không có module mới (loại T2) hay reformulation (loại T3).
- **Venue band:** Workshop / hội nghị Q4 / hội nghị Scopus-index. **Không phải Q1, không phải Q2-Q3 một mình.**
- **Điều kiện lên band cao hơn hiện không đạt:** cần (T2) một module kiến trúc mới thật sự khác — ví dụ: dùng chính lacunarity làm learnable pooling layer (S6 gợi ý, chưa ai làm cho AIGI detection) thay vì chỉ đặc trưng tĩnh — đây là hướng **future work**, không nằm trong phạm vi Q4 lần này.
- **Downgrade triggers:** Nếu sweep N cho thấy accuracy KHÔNG có xu hướng rõ ràng theo N (tương quan yếu/không có ý nghĩa thống kê với KS-stat), phần "cầu nối thực nghiệm" phải viết lại thành "quan sát sơ bộ, cần thêm dữ liệu" thay vì "chứng minh liên hệ" — tránh overclaim.
- **Confidence:** medium — phần verify tính khả thi (common.csv + scipy-only KS functions) là **cao** (đã xác nhận trực tiếp bằng code), nhưng kết quả tương quan thực tế (có ý nghĩa hay không) **chưa chạy nên chưa biết**.
- **Ledger:** C-1 (xem `notes/claims-ledger.md`)

---

## Xử lý bug LBP (G6) — khuyến nghị kỹ thuật cụ thể

Quan sát code trực tiếp (không phải suy đoán):
- `deepfake_pj_group (2).ipynb`: `local_binary_pattern(gray, P=8, R=1, method='uniform')`, bin vào `LBP_BINS=59`, range `(0,59)`.
- `deepfake_pj_group_FEATURE.ipynb`: cùng lời gọi nhưng `method='nri_uniform'`, cũng `LBP_BINS=59`.
- **Vấn đề toán học:** `method='uniform'` với P=8 chỉ sinh ra P+2=**10** mã phân biệt (0-9), không phải 59. Khi bin vào 59 slot, ~49/59 bin (≈26% của vector 187 chiều) **luôn = 0 một cách có cấu trúc** — không phải nhiễu ngẫu nhiên mà là lỗi chiều dữ liệu. Ngược lại `method='nri_uniform'` với P=8 sinh đúng P(P-1)+3=**59** mã — khớp chính xác với `LBP_BINS=59`.
- **Khuyến nghị đảo ngược so với action-plan hiện tại** (action-plan dòng 24 đề xuất chuẩn hoá về `'uniform'` — dựa trên lý do "tương thích OpenCV" — nhưng đây là hướng **kỹ thuật kém hơn** nếu giữ 59 bin): nên chuẩn hoá về `'nri_uniform'` (khớp `deepfake_pj_group_FEATURE.ipynb`), HOẶC nếu muốn giữ `'uniform'` thì phải sửa `LBP_BINS` xuống đúng 10, và **retrain lại toàn bộ pipeline + báo cáo lại 86.6%/0.94 sau khi sửa** (số hiện tại có thể thay đổi nhẹ vì ~26% chiều dữ liệu chết được loại bỏ hoặc thay bằng tín hiệu thật).
- Đây là điểm **Stop-Regain đã phát hiện trong phiên làm việc này**: `notes/deepfake-action-plan.md` (dòng 22-24) và `notes/deepfake-status-report.md` (dòng 79) mô tả **ngược** notebook nào dùng method nào — cả hai file cần sửa lại trước khi nhóm dùng làm tài liệu tham chiếu.

---

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| KS-test (Kolmogorov–Smirnov) | kiểm định KS | Đo mức khác biệt giữa 2 phân phối, cho ra thống kê d và p-value |
| PCA-residual | ảnh dư PCA | Ảnh sau khi loại bỏ N thành phần chính đầu, giữ lại phần "khó nén/ít tương quan" |
| Fractal Dimension (FD) | số chiều fractal | Độ đo mức độ phức tạp/gồ ghề hình học của tín hiệu ảnh |
| Multifractal Spectrum (MFS) | phổ đa fractal | Tập hợp số chiều fractal cục bộ theo tham số q, mô tả tính không đồng nhất |
| Lacunarity | độ rỗng (lacunarity) | Đo mức độ "lỗ hổng"/không đồng đều trong kết cấu ảnh, bổ sung cho FD |
| Local Binary Pattern (LBP) | mẫu nhị phân cục bộ | Mã hoá kết cấu cục bộ bằng so sánh pixel lân cận |
| nri_uniform | biến thể nri_uniform của LBP | Biến thể LBP không xoay-bất biến, sinh đúng P(P-1)+3 mã cho P điểm lân cận |

**Handoff:** dùng cho `notes/claims-ledger.md` (C-1) và báo cáo tổng hợp cuối (gobal-orchestrator report). Nếu nhóm quyết định chạy sweep N → cần `paper-method` (mode recipe) để viết pipeline tái lập chi tiết, hoặc `code-senior` để sửa bug LBP trực tiếp trong notebook.
