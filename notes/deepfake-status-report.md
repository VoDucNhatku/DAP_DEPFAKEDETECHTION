# STATUS REPORT — Deepfake Detection via PCA Residual + Handcrafted Features
> Ngày: 2026-07-08  |  Mục tiêu venue: **Q4 Workshop / Q3 Scopus Conference** (không Q1 — giải thích bên dưới)  |  Team: nhóm deepfake_pj  |  Author: Trieu Vy (ghi chép)

---

## 1. Mục tiêu chung của paper

Chúng ta đang xây một bài báo khoa học về **phát hiện ảnh deepfake** với phương pháp:
- PCA Residual: bóc tách high-frequency layer của ảnh bằng cách zero-out top-32 PCA components
- 187 handcrafted features (FFT 64 + LBP 59 + Noise 64) trên residual image
- 5 classifiers (Linear Regression / Random Forest / XGBoost / LightGBM / CatBoost)
- Kết quả hiện tại: **LightGBM Test Acc 86.6%, AUC 0.94**

---

## 2. Đánh giá Novelt Tier — Critical cho venue claim

| Tier | Định nghĩa | Áp dụng cho bài này? | Venue khả dụng |
|------|-----------|---------------------|----------------|
| **T1 — recipe** | Đổi công cụ / thêm classification mà paper gốc không có | **Đúng** — thay FreeAeon closed-source bằng FFT/LBP/Noise + chạy classifier | Q4 workshop, Q3 Scopus — **KHÔNG BAO GIỜ Q1 standalone** |
| T2 — module | Thay đổi module kiến trúc | Không | — |
| T3 — reformulation | Định nghĩa lại bài toán/quy trình | Không | — |

**→ Kết luận:** Core là **T1 recipe**. Theo rubric research-proposal-integracy §1: T1 → workshop/Q4; lên Q3 được nếu thêm điều kiện; lên Q1 cần T2/T3 + 2+ datasets + ablation + serious baselines — **không đủ với scope hiện tại**.
> ⚠️ **Điều này KHÔNG phải là hạn chế lớn** — nhiều paper tốt ở Q3/Q4 cũng là T1/T2 hybrid. Quan trọng là bạn **không claim Q1** trước khi đủ điều kiện.

---

## 3. Tình trạng hiện tại — Có gì / Không có gì

### 3.1 Đã có
| Khoản | Nguồn | Trạng thái |
|--------|-------|-----------|
| Dataset raw | `data/raw/` — 1M Fake Faces + FFHQ (đã resize 256x256) | ✅ Sẵn sàng |
| Pipeline Part A (download + face crop) | `deepfake_pj_group (2).ipynb` | ✅ Chạy được (đã chạy qua) |
| Pipeline Part B (extract FFT/LBP/Noise + ablation 7 variants) | `deepfake_pj_group_FEATURE.ipynb` | ⚠️ Có feature code, cần verify lại |
| Pipeline Part C (5 classifiers) | `model.ipynb` | ✅ Chạy được |
| Output files | `train.pkl / val.pkl / test.pkl / scaler.pkl` | ✅ Có sẵn (nhưng cần verify LBP consistency) |
| Ablation pkl | `train_ablation.pkl` (7 variants) | ⚠️ Có file — nhưng chưa chắc đã chạy đúng với notebook mới nhất |
| 5 model files | RF / XGB / LGBM / CAT + LR .pkl | ✅ Có |
| Result CSV | `model_results.csv` | ✅ Có |
| Paper gốc tham chiếu | `Research-Deepfake/` repo — báo cáo KS-test, PCA residual methodology | ✅ Đã phân tích |

### 3.2 Không có (đây là những gì Reviewer sẽ tấn công)
| Khoản | Tại sao quan trọng | Mức độ ưu tiên |
|--------|-------------------|---------------|
| **Ablation table (contribution từng nhóm feature)** | Nếu không có, bạn không chứng minh được FFT/LBP/Noise mỗi cái quan trọng thật → Reviewer: "tại sao dùng 3 nhóm?" | 🔴 P0 |
| **LBP method thống nhất** | 2 notebook dùng 2 method khác nhau (`uniform` vs `nri_uniform`) → output không reproducible cross-notebook | 🔴 P0 |
| **SOTA baseline comparison** | Không so sánh với Xception / EfficientNet → Reviewer: "kết quả 86% có thực sự tốt không?" | 🔴 P2 |
| **Related Work đầy đủ (≥10 papers)** | Desk Reject nếu Related Work hời hợt — reviewer biết nhiều paper bạn không trích dẫn | 🔴 P4 |
| **Theoretical Bridge: FFT/LBP ↔ Fractal** | FFT/LBP khác với Fractal descriptor — bạn cần lý thuyết để giải thích tại sao đổi tool mà vẫn bắt đúng tín hiệu | 🟠 P3 |
| **Robustness test** | Không có bảng JPEG/blur/noise → reviewer hỏi "method này robust không?" | 🟡 P1 |
| **Explain "PCA per-image (not global)"** | Không giải thích → nhìn như design oversight, không phải deliberate choice | 🟡 Nhỏ (1 paragraph) |
| **Reproducibility artifacts** | Code chưa clean + README + requirements.txt để reviewer có thể chạy lại | 🟡 Nhỏ |

### 3.3 Điểm mạnh hiện tại
- Pipeline end-to-end đã chạy được: raw → crop → feature → train → evaluate
- 5 classifiers cho thấy feature đã tốt (chỉ chênh nhau ~3% Acc giữa LR và LGBM)
- Có ablation pkl ready (chỉ cần verify lại)
- Có KS-test evidence từ paper gốc để support PCA residual story
- LR baseline 85.5% — bằng chứng feature linearly separable (điểm khá hiếm)

### 3.4 Điểm yếu hiện tại
- **Chưa chạy ablation table** → chưa biết mỗi nhóm feature đóng góp bao nhiêu
- **Chưa có SOTA baseline** → không đặt kết quả vào ngữ cảnh
- **LBP inconsistency** → có thể là source of hidden bug
- **Closed-source tool đã thay** → cần "cây cầu lý thuyết" để không mất hồn fractal
- **Không có robustness experiment** → không claim "robust" được
- **Không có Related Work** → mù văn cảnh

---

## 4. Con đường đạt Q4 — từ hiện tại đến submission

### Bước 1: P0 — Fix method + Ablation (tuần 1, thứ 2)
**Cần làm (chi tiết):**
1. Mở `deepfake_pj_group_FEATURE.ipynb`
2. Tìm dòng LBP: `lbp =局部二值模式(...)` — hiện tại đang `method='uniform'` (check lại)
3. Mở `deepfake_pj_group (2).ipynb`, tìm dòng LBP: đang `method='nri_uniform'`
4. **Quyết định team:** chọn 1 method. Khuyến nghị: `uniform` — phổ biến hơn, dễ hơn cho người khác reproduce.
5. Sửa cả 2 notebook về cùng 1 method.
6. Re-chạy pipeline:
   - Chạy lại extraction → có `train.pkl, val.pkl, test.pkl, scaler.pkl` mới
   - Chạy ablation → có `train_ablation.pkl` với đủ 7 variants:
     - `full` (187 dim)
     - `no_fft` (123 dim: LBP + Noise)
     - `no_lbp` (128 dim: FFT + Noise)
     - `no_noise` (123 dim: FFT + LBP)
     - `only_fft` (64 dim)
     - `only_lbp` (59 dim)
     - `only_noise` (64 dim)
7. Chạy classification trên mỗi variant → bảng kết quả: `variant | Acc | F1 | AUC`
8. Lưu kết quả vào `notes/ablation-results.csv`

**Checklist hoàn tất P0:**
- [ ] LBP method thống nhất giữa 2 notebook
- [ ] train.pkl / val.pkl / test.pkl / scaler.pkl mới
- [ ] train_ablation.pkl có đủ 7 keys với shape đúng
- [ ] Ablation results table (csv + một câu thảo luận)

**Ai làm:** 1 người chính, 1 người review
**Thời gian thực tế:** 30 phút chạy script + 15 phút verify

---

### Bước 2: P4 + P2 song song (tuần 1–2) — Related Work + SOTA baseline

#### 2.1 Related Work (P4)
**Làm thế nào:**
- Chia nhau đọc: mỗi người 4–5 papers
- Dùng Google Scholar với query:
  - "deepfake detection handcrafted features 2020 2021 2022 2023 2024"
  - "fractal dimension deepfake detection"
  - "lacunarity image forgery detection"
  - "PCA residual image classification"
  - "frequency domain deepfake detection"
- Lưu vào file `notes/related-work-papers.md` (mỗi paper: tên, năm, dataset, method, kết quả, điểm khác biệt với ours)

**Mục tiêu cuối:**
- ≥ 15 papers thu thập
- ≥ 10 papers đọc abstract / intro (high-quality)
- Synthesis paragraph 300–400 từ (không liệt kê tuần tự)
- Citation list đầy đủ (format: numbered theo IEEE hoặc APA)

**Ai làm:** 1–2 người
**Thời gian:** 2 buổi

---

#### 2.2 SOTA Baseline (P2)
**Chọn 2–3 baseline — đơn giản, có API sẵn:**

| Baseline | Làm sao | Ưu điểm | Effort |
|----------|---------|---------|--------|
| Xception (ImageNet pre-trained) | `tensorflow.keras.applications.Xception` | Nhẹ, phổ biến, reference point cho deepfake detection papers | ~1 buổi chạy + tune |
| EfficientNet-B0 | `tensorflow.keras.applications.EfficientNetB0` | Mới hơn Xception, nhẹ hơn ResNet | ~1 buổi |
| FaceForensics++ (nếu có số liệu) | Không cần chạy — lấy từ paper | Tiêu chuẩn mặc định cho deepfake benchmark | — |

**Protocol (phải giống nhau):**
- Dùng cùng ảnh đã crop 256x256 của bạn
- Split theo cùng stratified 80/10/10 (seed cố định)
- Fine-tune 15–20 epochs, batch size 32, AdamW
- Ghi: Train Acc / Val Acc / Test Acc / F1 / AUC / Params / Inference time (ms on CPU)

**Output:** Bảng `Method | Acc | F1 | AUC | Params | Inf ms` trong paper
**Ai làm:** 1 người chính + 1 người phụ
**Thời gian:** 1–2 ngày (chờ train TF model)

---

### Bước 3: P3 — Theoretical Bridge (tuần 2)
**Mục tiêu: trả lời câu hỏi "tại sao FFT/LBP/Noise bắt được tín hiệu fractal sau khi thay FreeAeon tool?"**

**Cách tiếp cận:**

*Bước 3a — Đọc (1 buổi):*
- Tìm papers về LBP như texture descriptor
- Tìm papers về Lacunarity definition (về "gap filling", "inhomogeneity")
- Đọc lại phần FFT/MFS trong paper gốc để hiểu MFS là gì

*Bước 3b — Viết (1–2 buổi):*
- Section: "Why Handcrafted Features Capture Fractal-Like Signals on Residual Images"
- Strategy: **không claim "tương đương"** — thay vào đó nói "FFT/LBP/Noise on residual acts as practical proxy capturing the same family of high-frequency statistical anomalies that fractal descriptors measure"
- Mỗi claim gắn tag:
  - [design] — "we reason that..." (cho phần lập luận logic của team)
  - [cited] — có paper trợ giúp
  - [derived] — có code/sanity check

**Output:** Paragraph 1–1.5 trang, với 2–3 citations
**Ai làm:** 1 người viết + 1 người review
**Thời gian:** 3–4 buổi (hoặc 2 buổi nếu skip correlation experiment)

---

### Bước 4: P1 — Robustness (tuần 2, song song) — Optional nhưng nên làm
**Cách làm — đơn giản, 1 buổi chạy:**
1. Lấy toàn bộ tập test
2. Apply từng perturbation (độ mạnh medium):
   - JPEG compression q=50
   - Resize 50%
   - Gaussian blur sigma=2
   - Gaussian noise N(0, 10)
3. Chạy best model (LightGBM) trên mỗi perturbed set
4. Ghi kết quả: `Perturbation | Clean Acc | Perturbed Acc | Degradation %`
5. Plot: bar chart

**Trong paper — cách nói:**
> "We evaluate stability of our pipeline under mild image corruption [ref]. Results in Table X show degradation of Y% under Z perturbation, indicating [honest interpretation]. This is not a robustness guarantee — a thorough adversarial robustness study is left for future work."
**Tuyệt đối không claim "robust"** — chỉ nói "stable under these specific conditions".

---

### Bước 5: Ghép nối + Viết Paper (tuần 3)
**Thứ tự viết:**
1. Abstract (tối đa 250 từ)
2. Introduction (1 trang)
3. Related Work (1 trang) — tổng hợp từ P4
4. Method (2–3 trang) — PCA residual + FFT/LBP/Noise + classifiers + ablation protocol
5. Experiment (2 trang) — dataset + setup + kết quả + ablation + SOTA compare + P1 robustness
6. Conclusion + Future Work (0.5 trang)
7. References

**Thứ tự code chạy lại để verify kết quả:**
- Chạy lại từ đầu train.pkl → model → kết quả → chụp log

---

## 5. Điểm cần thống nhất trong team (để không bị mâu thuẫn)

### Về PCA Residual
- Dùng **per-image PCA** (mỗi ảnh fit PCA riêng) — không phải global PCA trên toàn bộ dataset
- số PC zero-out = **32** (có thể nói sensitivity analysis: 24, 32, 64 được thử qua, 32 là giá trị median KS peak)
- Residual = `inverse_transform(img_transformed với top-32 = 0)` — giá trị uint8, range [0, 255]

### Về Feature
- LBP method: thống nhất chọn **`uniform`** (sau khi P0 fix)
- Noise: trích xuất từ 8 patch 8x8 → 64 bin histogram
- FFT: 64 bin histogram của magnitude spectrum (log scale)
- Total: 187 dim, StandardScaler, no PCA reduction

### Về Split
- Stratified 80/10/10, `random_state=42`, stratify theo label (real/fake)
- Giữ nguyên seed — KHI NÀO muốn reproduce cũng ra cùng kết quả

### Về Classifier
- 5 models, hyperparameter mặc định:
  - LinearRegression: threshold = 0.5
  - RandomForest: `n_estimators=200, random_state=42`
  - XGBoost: default
  - LightGBM: default
  - CatBoost: default
- Metric: Accuracy / F1 / AUC / Confusion Matrix
- **Kết quả chính để report:** LightGBM (Acc 86.6%, AUC 0.9427) — nhưng nhớ re-run sau P0 fix để confirm

---

## 6. Timeline đề xuất cho team

| Tuần | Thứ | Công việc | Phụ trách | Output |
|------|-----|-----------|-----------|--------|
| **Tuần 1** | Thứ 2 sáng | P0: Thống nhất LBP method, re-chạy pipeline, verify ablation | A | train/test/val/scaler pkl mới |
| | Thứ 2 chiều | P4: Related Work search — mỗi người 4 papers | Tất cả | notes/related-work-papers.md |
| | Thứ 3 | P2: Setup TF + train Xception baseline | B | Model + log |
| | Thứ 4 | P2: Train EfficientNet baseline + ghi so sánh | B | Bảng SOTA |
| | Thứ 5 | P4: Synthesis paragraph Related Work + bắt đầu Method section | A | Draft paragraph 300 từ |
| **Tuần 2** | Thứ 1 | P3 (Bước 1): Đọc papers về LBP/Lacunarity bridge | C | Ghi chú |
| | Thứ 2 | P3 (Bước 2): Viết Theoretical Bridge section | C | Draft section 1 trang |
| | Thứ 3 | P1: Chạy 4 perturbation experiments | A | Bảng robustness |
| | Thứ 4 | P3 (review): Review lại bridge section + Ablation table | B + C | Polished |
| | Thứ 5 | P4: Hoàn tất Related Work + verify citations | A | Related Work section hoàn chỉnh |
| **Tuần 3** | Thứ 1–2 | Draft Method + Experiment | B | Draft Method |
| | Thứ 3 | Viết Introduction + Conclusion | C | Draft Intro/Concl |
| | Thứ 4 | Review cross-team: tất cả đọc draft, góp ý | Tất cả | Review notes |
| | Thứ 5 | Final polish + verify tất cả số liệu | Tất cả | Draft gần final |

**Nhân sự đề xuất:**
- **A** (phụ trách method + robustness): người mạnh về xử lý ảnh / Python
- **B** (phụ trách baseline SOTA + draft Method/Experiment): người mạnh về ML / TF
- **C** (phụ trách bridge + Related Work + Intro/Conclusion): người mạnh về đọc paper / viết tiếng Angn

*Nếu team có ít hơn 3 người: gộp trách nhiệm. P2 (SOTA baseline) là phần tốn thời gian nhất — nên ưu tiên.*

---

## 7. Checklist "Đủ điều kiện submit cho Q4" — team check

| Tiêu chí | Đã đủ? | Nguồn / Cần làm gì |
|-----------|--------|-------------------|
| Core idea + PCA residual explanation trong Method | ⬜ | Viết khi draft Method |
| 187-dim feature description (FFT/LBP/Noise) | ⬜ | Viết trong Method |
| Ablation table (7 variants) | 🔴 **Chưa có** | Cần P0 |
| SOTA baseline comparison table | 🔴 **Chưa có** | Cần P2 |
| Main results table (5 classifiers) | ✅ | Có sẵn, verify lại sau P0 |
| Robustness table (optional) | 🟡 Nên làm | P1 |
| Figure: Residual vs original visualization | ⬜ | Cần plot |
| Figure: KS-score theo PCA_n | ⬜ | Có trong main.ipynb, cần export |
| Figure: Results bar chart (5 models) | ✅ | Có trong model.ipynb |
| Figure: Confusion matrix best model | ✅ | Có sẵn |
| Related Work section (10+ papers) | 🔴 **Chưa có** | Cần P4 |
| Theoretical Bridge section | 🔴 **Chưa có** | Cần P3 |
| Reproducibility: code release hoặc appendix đủ | 🟡 Cần clean | P0 sau đó |
| Paper draft đầy đủ 6 sections | ⬜ | Tuần 3 |

---

## 8. Review phản biện — 5 hiểm cảnh + đáp án mẫu

Để team luyện tập trước khi nộp:

### 1. "Tại sao không dùng SOTA (Swin / EfficientNet) — kết quả 86% có thực sự tốt?"
> Đáp: "Mục tiêu của chúng tôi là lightweight explainable detection, không phải đuổi accuracy tuyệt đối. Trong Table X chúng tôi so sánh với [baseline], kết quả của chúng tôi cách 2–4% nhưng chạy trên CPU trong ms."

### 2. "FFT/LBP thay vì Fractal — liệu có mất tín hiệu quan trọng không?"
> Đáp: "Chúng tôi lập luận FFT/LBP/Noise trên residual là practical proxy cho fractal descriptors (xem Section X). Tuy nhiên, đây là [design]-level claim — chúng tôi không khẳng định tương đương toàn phần mà chỉ nói 'bắt cùng family of anomalies'."

### 3. "PCA per-image thay vì global — có ổn không?"
> Đáp: "Per-image PCA là deliberate choice: chúng tôi quan tâm đến artifact trong từng ảnh, không phải variance cross-image. Global PCA sẽ bị trung bình hóa và mất signal."

### 4. "Tại sao không so với paper gốc của tác giả?"
> Đáp: "Paper gốc [ref] dùng FreeAeon tools + chỉ phân tích thống kê KS-test, không có classification experiment. Bảng accuracy của chúng tôi là contribution mới. So sánh trực tiếp khó vì protocol khác nhau, nhưng trend histogram overlap của chúng tôi phù hợp với KS trend mà paper gốc báo cáo."

### 5. "Method robust không? Nếu generator cải tiến giảm high-frequency artifact thì sao?"
> Đáp: "Nhóm chúng tôi công nhận đây là limitation rõ ràng (xem Future Work). Hiện tại với GAN/Diffusion model phổ biến, residual có divergence. Nếu các generator tương lai theo chiều hướng giảm high-frequency residual, phương pháp này sẽ suy giảm — trong tương lai chúng tôi dự định kết hợp với learning-based layer để tăng robustness."

---

## 9. Venue tham khảo — nên target ở đâu?

| Venue hạng mục | Phù hợp? | Lý do |
|----------------|----------|-------|
| CVPR / ICCV / ECCV (Q1) | ❌ Không với scope hiện tại | Cần T2/T3 + 2+ datasets + full ablation |
| IEEE TIP / TIFS (Q1 journal) | ❌ Không với scope hiện tại | Tương tự |
| ICIP / ICPR / WACV (Q2–Q3) | ❌ Có thể đủ nếu thêm 1 dataset phụ | Cần ablation + SOTA baseline |
| **ViTsing Workshop / ICME workshop** | ✅ **Đủ với P0+P2+P4** | Workshop thường có standard: clear method + some baseline |
| **Scopus Q3 regional conference** | ✅ **Đủ nếu thêm P3** | Yêu cầu có lập luận rõ, không cần SOTA mạnh |

> **Khuyến nghị:** Nhắm **1 workshop track** tại CVPR/ICCV/ECCV (có deadline xa hơn, dễ hơn) + **1 Scopus Q3 regional conference** song song. Nếu P3 đã xong thì cả 2 đều đủ.

---

## 10. Câu hỏi cần team họp thảo luận

1. **P0 — LBP method:** Chọn `uniform` hay `nri_uniform`? (Cần nhất trí)
2. **P2 — SOTA baseline:** Xception / EfficientNet / FaceForensics++ benchmark — chọn cái nào?
3. **P3 — Theoretical Bridge:** Có muốn làm đến mức correlation experiment (Pearson) không, hay chỉ giữ phần lý thuyết viết thôi?
4. **P1 — Robustness:** Làm chi tiết 4 perturbations hay chỉ làm 2 trivial (JPEG + blur)?
5. **Code release:** Có muốn push code lên GitHub công khai trước khi submit không? (Nhiều venue giờ yêuầu)
6. **Authorship:** Ai làm first author? Ai làm corresponding? (Nên quyết định sớm)

---

## Tài liệu tham chiếu

| File | Nội dung |
|------|----------|
| `Research-Deepfake/src/main.ipynb` | Paper gốc — KS-test, phân tích PCA Residual |
| `Research-Deepfake/src/feature.py` | FreeAeon tool usage — reference để hiểu tool thay thế |
| `Research-Deepfake/src/pipeline.sh` | Pipeline flow — reference |
| `deepfake_pj_group (2).ipynb` | Pipeline nhóm Part A+B — cần P0 fix |
| `deepfake_pj_group_FEATURE.ipynb` | Ablation variants — cần P0 verify |
| `model.ipynb` | Part C — 5 classifiers |
| `notes/deepfake-action-plan.md` | Plan chi tiết từng bước |
| `notes/deepfake-status-report.md` | **File này** — tổng trạng team |

---

*Last updated: 2026-07-08 by gobal-orchestrator / Trieu Vy (review)*
*Next review: sau khi P0 hoàn tất (dự kiến cuối tuần 1)*
