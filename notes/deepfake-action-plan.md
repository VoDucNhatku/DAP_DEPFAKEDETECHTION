# Deepfake Detection Paper — Detailed Action Plan
> Ngày tạo: 2026-07-08  |  Target venue: Q4 workshop / Q3 Scopus conference
> Core novelty tier: **T1 — recipe** (closed-source tool replacement + classification evaluation added)

---

## 0. Guiding principles

The rule of this plan: **must-have → should-have → nice-to-have**.
- Must Have fail → paper bị **desk reject** dù nội dung có hay.
- Should Have mancla → paper "chạy được" nhưng thiếu hồn.
- Nice to Have vắng mặt → paper không bị từ chối, nhưng không có điểm nhấn.

Tất cả các hạng mục có thể giải quyết được. Không có bẫy kỹ thuật —— đây là plan dành cho một nhóm sinh viên có Notebook Python + dataset.

---

## 1. Must-have (ticket vào cửa — không có 1 cái nào cũng bị loại)

### P0 - Fix method bug + finalize feature pipeline
**Cần làm:**
1. Mở `deepfake_pj_group_FEATURE.ipynb`
2. Kiểm tra dòng LBP configuration: hiện tại notebook này dùng `method='uniform'`, trong khi `deepfake_pj_group (2).ipynb` dùng `method='nri_uniform'`
3. Thống nhất chọn **1 method** (khuyến nghị `uniform` —— tương thích cao hơn với OpenCV document, dễ reproduce)
4. Re-chạy pipeline: `extract → ablation → scale → split → save 7 pkl`
5. Verify các 7 file ablation tương ứng mỗi variant đều có shape đúng

**Output chờ:**
- `train.pkl / val.pkl / test.pkl / scaler_pkl` (updated)
- `train_ablation.pkl` với 7 keys đúng

**Ai phụ trách:** 1 người
**Thời gian:** 30 phút
**Rủi ro:** Thấp — chỉ sửa 1 parameter

**Lý do bắt buộc:**
- Nếu bạn nộp và reviewer chạy code nhận ra output shape mismatch / LBP method khác nhau giữa 2 notebook → ngay lập tức nghi ngờ toàn bộ experiment reproducibility.
- Hiện chưa chạy ablation → bạn không biết thực tế FFT / LBP / Noise mỗi cái đóng góp bao nhiêu → không cơ sở cho claim "cả 3 nhóm đều quan trọng".

---

### P2 - Thêm 2–3 SOTA baseline trên cùng dataset

**Cần làm:**
1. Chọn **2–3 baselines** đơn giản, không cần train lại từ đầu:
   - (a) **Xception** — Keras `applications.Xception`, pre-trained on ImageNet, fine-tune 10–15 epochs. Cài `tensorflow` — gọn.
   - (b) **EfficientNet-B0** — tương tự, TF Keras.
   - (c) **FaceForensics++ benchmark** nếu có sẵn số liệu trong literature (không cần chạy).
2. Train trên tập bạn đã có (có thể dùng lại ảnh đã crop — bỏ bước PCA residual, cho raw hoặc sau blur resize)
3. Ghi lại Acc / F1 / AUC / thời gian inference

**Output chờ:**
- Bảng so sánh: `Method | Acc | F1 | AUC | Params | Inference time (ms)`
- 1-2 câu thảo luận: tại sao phương pháp của bạn thấp hơn hay cao hơn

**Ai phụ trách:** 1 người chính + 1 người phụ
**Thời gian:** 1–2 ngày (chủ yếu chờ train TF model)

**Lý do bắt buộc:**
- Reviewer chuyên về deepfake sẽ tự hỏi: "Tại sao không so với Xception?" — nếu bạn không có trong paper, bạn trông thiếu bài bản.
- SOTA comparison tạo **ngữ cảnh** cho số liệu 86.6% —— "trong tầm 2–4% của SOTA nhẹ mà không cần GPU" là claim bạn có thể bảo vệ.
- Nhẹ (Không cần dùng toàn bộ code của SOTA —— chỉ cần API gọi, thường ~20 dòng).

---

### P4 - Related Work scan ~15 papers

**Cần làm:**
1. Đặt phạm vi: 2019–2026, tìm papers về:
   - Deepfake detection using frequency domain / artifact
   - Handcrafted feature approaches (FD, Lacunarity, texture descriptors)
   - PCA-based pre-processing cho detection
   - Xác định 5–8 papers "phải trích dẫn" (highly cited trong các survey)
2. Mỗi paper annotate: năm, dataset dùng, method, kết quả, **điểm khác biệt với approach của bạn**
3. Organize Related Work theo logic:
   - (A) Phương pháp học sâu (SOTA) —— "black-box, performance cao nhưng heavy"
   - (B) Phương pháp handcrafted (FD / Lacunarity / texture-based) —— "phân tích fractal trực tiếp, closed-source tool limitation"
   - (C) Phương pháp residual / frequency-based —— "gần nhất với chúng tôi nhưng không dùng PCA residual + classification end-to-end"
4. Viết bài tổng hợp (synthesis) paragraph, không liệt kê tuần tự

**Output chờ:**
- Bảng 15 papers (góc nhìn nhanh)
- Paragraph synthesis ~300–400 từ
- Citation list đầy đủ + [unverified] tags nếu chưa verify xong

**Ai phụ trách:** 1 người
**Thời gian:** 1–2 buổi (search + đọc abstract + ghi chú)

**Lý do bắt buộc:**
- Related Work hời hợt → Desk Reject ngay. Reviewer hỏi: "Bạn đã đọc [paper X] chưa? Nó có cùng approach ma bạn không trích dẫn".
- Related Work synthesis tốt → reviewer đọc thấy bạn hiểu văn cảnh.

---

## 2. Should-have (quyết định paper có hồn hay không)

### P3 - Xây "cây cầu lý thuyết" (Theoretical Bridge Section)
**Vấn đề cần giải thích:**
> "FFT / LBP / Noise là các descriptors thông dụng, Fractal Dimension / MFS / Lacunarity là các descriptors fractal chuyên biệt. Làm sao bạn khẳng định rằng FFT/LBP/Noise bắt được **cùng loại tín hiệu** mà FreeAeon tool bắt được?"

**Lộ trình chi tiết:**

**Bước 1 (1 buổi — đọc):**
- Tìm 2–3 papers về **Lacunarity as texture descriptor** (đọc abstract)
- Tìm 1–2 papers về **LBP ↔ statistical texture** mối quan hệ
- Ghi chú: các định nghĩa LBP trên local window có vai trò gì với homogeneity measurement

**Bước 2 (1–2 buổi — viết):**
- Viết section ngắn (1–1.5 trang) "Why FFT/LBP/Noise on Residual Captures Fractal-Like Signals":
  - FFT on residual ≈ spectrum of high-frequency component (correlation với MFS —— measure spectrum scaling)
  - LBP (uniform) trên local patch ≈ local texture homogeneity measurement ≈ Lacunarity's definition of gap filling ratio
  - Noise statistics ≈ measure of local randomness ≈ Fractal Dimension's roughness measure
- Lưu ý: trình bày dạng **"these are practical proxies, theoretically related to..."** — không claim "chính xác tương đương".

**Bước 3 (tùy chọn — 1 buổi):**
- Chạy correlation experiment: nếu bạn vẫn có data / quyền truy cập output FreeAeon từ paper gốc, tính Pearson correlation giữa 187-dim feature vector và FD/MFS vector trên cùng ảnh.
- Nếu Pearson > 0.6 → bạn có data để claim "empirically correlated".

**Ai phụ trách:** 1 người viết + 1 người review
**Thời gian:** 3–4 buổi (2 đọc + 2 viết) hoặc 2 buổi nếu skip Bước 3

**Lưu ý quan trọng (theo research-proposal-integrity §4):**
- Nếu viết section này, phải gắn **provenance tag** cho mỗi claim:
  - **[derived]** cho phần lập luận logic của các bạn
  - **[cited]** cho phần tham chiếu papers đọc được
  - **[design]** cho phần "chúng tôi lập luận rằng..." mà chưa có citation trực tiếp
- Không phras [design] claim với confidence level của [derived].

---

## 3. Nice-to-have (điểm cộng — không làm cũng passed nhưng có thì tốt hơn)

### P1 - Robustness test (3–4 perturbations)

**Bộ perturbation đơn giản — chạy trong 1 buổi:**

| Perturbation | Cách thực hiện | Kiểm tra |
|--------------|---------------|----------|
| JPEG compression | `cv2.imwrite(..., [cv2.IMWRITE_JPEG_QUALITY, 50])` | Accuracy degradation |
| Resize 50% | `cv2.resize(img, (img.shape[1]//2, img.shape[0]//2))` | Accuracy degradation |
| Gaussian blur | `cv2.GaussianBlur(img, (5,5), sigma=2)` | Accuracy degradation |
| Gaussian noise | `img + N(0, 10) noise, clip về [0,255]` | Accuracy degradation |

**Định dạng output:**
- Bảng: `Perturbation | Clean Acc | Purturbed Acc | Degradation %`
- Plot: bar chart hoặc line chart

**Cách trình bày trong paper:**
- Một paragraph trong phần Experiment:
  > "To evaluate stability of our handcrafted features under mild image corruption, we apply four common perturbations [ref] at moderate severity. Results in Table X show that..."
- **KHÔNG** claim "robust to all attacks" — chỉ nói "stable under these specific perturbations at this severity".

**Ai phụ trách:** 1 người
**Thời gian:** 1 buổi
**Rủi ro:** Nhớ thêm paragraph giải thích tại sao không chạy adversarial attack (cần chuyên sâu, out-of-scope).

---

## 4. Timeline gantt (tuần)

```
Tuần 1
├── Thứ 2: P0 — Thống nhất LBP method + re-chạy pipeline (30 phút)
├── Thứ 2 chiều: P4 — Start Related Work scan (đọc 5 papers)
├── Thứ 3: P2 — Setup TF + train first SOTA baseline
├── Thứ 4: P2 — Train second baseline, ghi kết quả
└── Thứ 5: P4 — Continue scan + bắt đầu synthesis paragraph

Tuần 2
├── Thứ 1: P3 (Bước 1) — Đọc papers về Lacunarity / LBP relationship
├── Thứ 2: P3 (Bước 2) — Viết Theoretical Bridge section
├── Thứ 3: P1 — Chạy 4 perturbation experiments
├── Thứ 4: P3 (Bước 2 tiếp) — Hoàn thiện + review lại
└── Thứ 5: P4 — Hoàn tất Related Work, verify citations

Tuần 3
├── Thứ 1–3: Draft paper (Introduction + Method + Experiment) dựa trên
│              kết quả Tuần 1-2
├── Thứ 4: Internal review — cross-check kết quả, sổ claim ledger
└── Thứ 5: Polishing + mục tiêu submit trước deadline venue
```

---

## 5. Reviewer-rejection matrix (ánh xạ rủi ro)

| Vấn đề reviewers thường hỏi | Hạng mục giải quyết | Nếu không giải quyết → mức độ |
|------------------------------|----------------------|-------------------------------|
| "Code không reproduce được" | P0 | 🔴 Desks Reject |
| "Không so với SOTA nào cả" | P2 | 🔴 Major / Đá về sửa |
| "Related Work thiếu [paper X] mà tôi biết" | P4 | 🟠 Major |
| "Feature FFT/LBP không liên quan gì đến Fractal" | P3 | 🟠 Major (đánh giá "không hiểu bài") |
| "Tại sao không chạy ablation?" | P0 | 🟡 Minor (nhưng nếu không trả lời được → tín hiệu yếu) |
| "Tại sao không so với paper gốc của tác giả?" | P2 | 🟡 Minor |
| "Method có robust không?" | P1 | 🟡 Minor |
| "PCA per-image thay vì global, explain?" | N/A — chỉ cần 1 paragraph trong Method | 🟡 Minor |

---

## 6. Checklist trước khi submit

- [ ] P0 hoàn tất: code chạy clean, LBP method thống nhất
- [ ] P0 hoàn tất: ablation table có đủ 7 variant
- [ ] P2 hoàn tất: 2–3 SOTA baseline đã chạy xong + bảng so sánh
- [ ] P4 hoàn tất: Related Work đọc ≥ 10 papers, synthesis paragraph viết xong
- [ ] P3 hoàn tất: Theoretical Bridge section có ít nhất 1 paragraph mạnh
- [ ] P1 (nếu làm): Robustness table 3–4 perturbations
- [ ] Paper draft: Abstract / Intro / Related Work / Method / Experiment / Conclusion đầy đủ
- [ ] Figure gallery: ≥ 4 hình (residual visualization, KS plot, results bar chart, confusion matrix)
- [ ] Bảng kết quả chính (5 classifiers) + SOTA comparison + ablation
- [ ] Notes / claims-ledger.md cập nhật (venue claim, tier grading, revocation protocol)
- [ ] Verify tất cả metrics trùng với log file (no fabricated numbers)
- [ ] Repo / code sẵn sàng release (GitHub repo link trong paper) HOẶC appendix có đủ để reviewer reproduce

---

## 7. Venue Target Recommendation (tính đến 2026-07-08)

### Tier phù hợp nhất:
**T1 — recipe** với điều kiện bổ sung → **Q4 Workshop / Scopus Q3 regional conference**

### Điều kiện để duy trì / nâng cấp:
- Q4 workshop yêu cầu: must-have P0 + P2 + P4 đầy đủ. Should-have P3 là optional.
- Q3 Scopus conference yêu cầu: must-have + should-have P3 + ít nhất một dataset phụ (hoặc 1 SOTA baseline nghiêm túc).
- Lên Q2: cần T2 hoặc T3 element thêm vào (không đủ với contribution hiện tại).
- Đi lên Q1: cần reformulation (T3) hoặc rất nhiều bổ sung: 3+ datasets, full ablation, extensive baselines, 10+ papers related work scan.

### Lý thuyết có thể bị từ chối (Downgrade triggers):
1. Nếu reviewer phát hiện PCA residual không thực sự gắn với fractal property → downgrade T1
2. Nếu FFT/LBP/Noise chỉ bắt noise thông thường (không phải AI artifact) → claim về "deepfake fingerprint" sụp đổ
3. Nếu paper gốc của tác giả đã publish {đang kiểm tra} —— nếu paper gốc đã chứa classification experiment với kết quả cao hơn → nhóm bạn không có novelty nữa (cần verify)

---

## 8. Appendix: Nguồn lực tham khảo

### Papers cần đọc cho P3 (Theoretical Bridge):
- [ ] "Lacunarity as a texture descriptor" — tìm qua Google Scholar
- [ ] "Local Binary Patterns for texture classification" — Ojala et al. (classic, đã có kiến thức)
- [ ] "Fractal Dimensions and Lacunarity: complementary tools for texture analysis" — review paper
- [ ] "[cần tìm] FFT for deepfake detection — các papers dùng spectrum analysis"

### Papers benchmark cho P2 (SOTA baseline):
- [ ] "FaceForensics++: Learning to Detect Manipulated Facial Images" — Rössler et al. 2019
- [ ] "Deepfake Detection Using Frequency Domain Analysis" — nhiều version, tìm 1-2
- [ ] "[cần chọn] một paper cận giới: handcrafted + learning hybrid, gần với approach của bạn nhất"

### Repo / tool:
- `D:\CPV-VIP\Research-Deepfake\` — paper gốc + code
- `D:\CPV-VIP\deepfake_pj_group (2).ipynb` — pipeline nhóm (A+B)
- `D:\CPV-VIP\deepfake_pj_group_FEATURE.ipynb` — ablation variants
- `D:\CPV-VIP\model.ipynb` — classifier C

---

## 9. Claim governance trước khi nộp

Theo `~/.claude/rules/research-proposal-integrity.md` §3, mọi novelty/venue claim cần được ghi vào `notes/claims-ledger.md` trước khi trả lời follow-up. Trước khi submit paper:

1. Review tất cả claims trong draft:
   - "T1 recipe" — đã document
   - "Q4/Q3 venue" — đã ghi nơi nào, với điều kiện gì
   - Các claim con trong Introduction / Experiment / Conclusion

2. Từng claim phải có provenance tag:
   - numbers → trùng với log file
   - claims lý thuyết → hoặc [cited] (có reference) hoặc [design] (với disclaimer)

3. Ghi revision nếu plan thay đổi trong quá trình làm.

---

*Kế hoạch này được tạo bởi gobal-orchestrator. Cập nhật theo tiến độ thực tế của team.*
