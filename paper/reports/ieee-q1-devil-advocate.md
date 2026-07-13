# IEEE Q1 Devil's Advocate Review — main.md

**File:** `D:\CPV-VIP\paper\main.md` (194 dòng)
**Khâu:** `ieee-q1-devil-advocate` — Task #21, bước 5/6 trong pipeline `paper-writing-integrity.md` §6
**Khâu trước:** `latex-fix` — PASS (xem `paper/reports/latex-fix.md`)
**Ngày:** 2026-07-14
**Hiệu chỉnh phản biện:** rigor soi xét ở mức Q1 IEEE Transaction-family, nhưng bar PASS/FAIL được calibrate đúng venue band THẬT đã chấm trong `notes/claims-ledger.md` (dòng C-1 + C-2): T1, Workshop / hội nghị Q4 / Scopus-index — **không phải Q1**.

---

## Q1 IEEE Devil's Advocate Review

### Reviewer Summary

| Metric | Value |
|---|---|
| Paper Assumed Target (để soi rigor) | IEEE Q1 (Transaction/TPL/JBHI-style) |
| Venue Claim Thực Tế (claims-ledger C-1/C-2) | Workshop / hội nghị Q4 / Scopus-index |
| Review Date | 2026-07-14 |
| Overall Disposition — theo tiêu chuẩn Q1 giả định | **Major Reject** |
| Overall Disposition — theo venue band thật đã chấm | **PASS** (sau khi 5 lỗi bên dưới đã được sửa và verify ngay trong lượt review này) |

---

## Sửa lỗi đã áp dụng trong chính lượt review này (FAIL→FIX loop-back, §6)

Pipeline `paper-writing-integrity.md` §6 quy định: một FAIL phải quay lại khâu sinh ra nó trước khi chuỗi đi tiếp. Vì không dùng sub-agent (chạy inline một mình), 5 lỗi phát hiện được trong lượt đọc đối kháng dưới đây đã được sửa trực tiếp vào `main.md` ngay trong turn này, không chỉ báo cáo suông. Mọi con số sửa đều đối chiếu trực tiếp với Table 1 (dòng 133-139) — không suy đoán.

| # | Dòng | Lỗi gốc | Đã sửa thành | Băng chứng |
|---|---|---|---|---|
| A | 145 (+ dòng 11 Abstract) | §6.2 viết LightGBM giữ "best test F1" và "best test AUC" | XGBoost thắng cả 3 test metric (Acc 0.8688, F1 0.8687, AUC 0.9442); LightGBM chỉ thắng cả 3 validation metric | Table 1: cột Test F1/Test AUC của XGBoost (0.8687/0.9442) cao hơn LightGBM (0.8664/0.9427) — mâu thuẫn trực tiếp giữa bảng và văn xuôi của chính bài |
| B (miscount) | 31 | "Two recent studies" nhưng liệt kê 3 nghiên cứu (Yasir&Kim [4], Nirob et al. [9], Chaudhari et al. [10]) | "Three recent studies" | Đếm trực tiếp số nghiên cứu được nêu tên trong câu |
| C (jargon leak) | 35 | "...consistent with the recipe-level (T1) novelty tier we claim in Section 5" — "T1" là thuật ngữ chấm điểm nội bộ chưa từng định nghĩa trong bài; Section 5 là Experimental Setup, không bàn novelty | Viết lại không dùng "T1", không có cross-reference gãy | Section 5 (dòng 113-123) xác nhận không có đoạn nào bàn về novelty tier |
| D (precision) | 141 | "within 0.002 of AUC" | "within roughly 0.003 of AUC" | Table 1: gap Val/Test AUC thực tế — RandomForest 0.0023, XGBoost 0.0027, CatBoost 0.0026 — cả 3 đều vượt ngưỡng 0.002 đã tuyên bố |
| E (title-scope gap) | 153 (câu mới chèn vào §6.3) | Tiêu đề bài có "Reproducible" nhưng §5/§6.3 gốc chỉ khóa seed cho data-split, chưa nói gì về tính ngẫu nhiên nội tại của 5 classifier (vd. bootstrap của RandomForest) hay việc pin phiên bản thư viện | Thêm câu công khai đúng phạm vi: reproducibility claim chỉ phủ split + PCA, không phủ random nội bộ classifier/library version | §5 dòng 123 xác nhận "hai lần chạy độc lập" chỉ nói về pipeline của nhóm, không đề cập bên thứ ba trên máy/thư viện khác |

Toàn bộ 5 sửa đổi đã được đọc lại trực tiếp (Read) sau khi Edit, xác nhận nội dung đúng và đọc tự nhiên trong ngữ cảnh xung quanh — không chỉ tin vào thông báo "success" của tool.

---

### 1. Novelty Assessment (40% weight)

- **Position in literature:** Bài đóng một khoảng trống thực nghiệm cụ thể của [1] (Xie et al., arXiv:2604.17268) — bài gốc thiết lập PCA-residual + mô tả fractal đóng (FreeAeon FD/MFS/Lacunarity) + kiểm định KS như một tín hiệu phân biệt thật/giả, nhưng **chưa từng chạy một classifier thật nào** trên residual đó (verify: §1 Introduction dòng 15-23, mô tả gap này). Bài hiện tại thay mô tả đóng bằng ba descriptor mở (FFT+LBP+noise, dòng 61-67) và bổ sung bài toán phân loại nhị phân thật với 5 classifier (Table 1).
- **Closest prior work — hai lớp so sánh riêng biệt (một reviewer Q1 sẽ ép hỏi cả hai, không được gộp làm một):**
  - **(a) Bài đang được mở rộng:** [1] Xie et al. — khác trục: bài này không đụng đến fractal descriptor, không dùng KS-test, chỉ giữ lại bước PCA-residual (N=32, kế thừa nguyên default của [1], §5 dòng 119) và thay toàn bộ phần trích đặc trưng + thêm bài toán classification.
  - **(b) Tiền lệ phương pháp luận gần nhất:** [4] Yasir & Kim (arXiv:2502.11763) — cùng dạng "recipe": đặc trưng thủ công + ensemble ML cổ điển cho phân loại nhị phân real/fake khuôn mặt. Khác biệt ở cấp thành phần, xác nhận trực tiếp qua dòng 31: [4] dùng HOG+LBP+KAZE trên **ảnh gốc**; bài này dùng FFT+LBP+noise-residual trên **ảnh PCA-residual**. Đây là khác biệt thật (feature set khác, tầng tiền xử lý khác), không phải vỏ bọc đổi tên.
  - **(c) Tiền lệ gần nhì:** [9] Nirob et al. (arXiv:2601.19262) — handcrafted-fusion+LightGBM, khác dataset (CIFAKE thay vì FFHQ+StyleGAN-fake).
- **Novelty tier theo rubric integrity:** **T1 (recipe)** — xác nhận qua đọc trực tiếp §4 Method: không có module kiến trúc mới, không có công thức bài toán mới, chỉ là thay thế công thức trích đặc trưng + tái sử dụng classifier có sẵn nguyên bản (RandomForest/XGBoost/LightGBM/CatBoost mặc định, §4.4 dòng 111). Khớp hoàn toàn với tự chấm của `claims-ledger.md` C-1/C-2. Không tìm thấy chỗ nào trong bản thảo (sau các sửa ở trên) thổi phồng thành T2/T3 — `style-humanizer` đã loại "paradigm"-style wording ở khâu trước, và sửa lỗi C ở trên loại nốt mảnh jargon-tier còn sót.
- **Ledger cross-check:** **PASS.** C-1: T1 → Workshop/hội nghị Q4/Scopus-index, "không phải Q1, không phải Q2-Q3 một mình". C-2 (dòng con, phạm vi thực tế của chính bản thảo này) liệt kê đúng những gì đã hoàn thành (LBP nri_uniform, pipeline 187 chiều, 5 classifier chạy 2 lần độc lập, 15 nguồn Related Work) và đúng những gì còn là Future Work (sweep N, ablation PCA-vs-raw, robustness test) — đối chiếu trực tiếp với §6.3/§7 của main.md, không có mục nào trong bản thảo claim vượt quá những gì C-2 cho phép.
- **Incremental hay disruptive:** Incremental — chính bài tự nhận thức đúng mức trong §7 (dòng 157): "a fixed-recipe contribution," không phải "an architectural one," và nêu rõ con đường nâng cấp lên T2 (thay lacunarity bằng learnable pooling layer theo [6]) như một hướng tương lai dài hạn, chưa làm. Một bài tự định vị đúng trần novelty của chính nó là điều hiếm và đáng ghi nhận, không phải điểm trừ.
- **Novelty verdict:** **FAIL dưới bar Q1** (T1 một mình không đủ Q1 theo hard rule của `research-proposal-integrity.md` §1 — không có ngoại lệ). **PASS dưới venue band thật đã claim** (Workshop/Q4/Scopus), vì T1 đủ điều kiện ở band đó theo đúng rubric.

### 2. Ablation Study Check (30% weight)

- **Module breakdown table:** Bài **không có** ablation cấp thành phần nào — không có so sánh PCA-residual-vs-raw, không có leave-one-descriptor-out (chỉ-FFT / chỉ-LBP / chỉ-noise). Phần "so sánh" duy nhất tồn tại là so sánh 5 CLASSIFIER trên cùng một vector 187 chiều cố định (Table 1) — đây là model comparison, không phải ablation đặc trưng, và bài không hề lẫn lộn hai khái niệm này (verify: §6.1-6.2 không dùng từ "ablation" cho phần classifier comparison).
- **Baseline sanity:** Baseline hồi quy tuyến tính có ngưỡng (§6.2 dòng 149, đã verify qua Table 1: Test Acc 0.8552, chỉ kém ~1.5 điểm % so với boosted tree tốt nhất) là một tín hiệu gián tiếp có giá trị — gợi ý phần lớn tín hiệu phân biệt nằm ở bản thân đặc trưng chứ không phải độ phức tạp classifier. Đây là baseline sanity hợp lệ nhưng **không thay thế được** một ablation thật.
- **Ablation table adequacy:** **FAIL dưới Q1** — thiếu hoàn toàn ablation cấp module gần như chắc chắn bị desk-reject tại venue Transaction-family. **ACCEPTABLE-AS-DISCLOSED dưới band Q4/Workshop** — `claims-ledger.md` C-2 cho phép rõ ràng phạm vi này, và bản thảo (đã verify trực tiếp §6.3 dòng 153 + §7 dòng 157) không một chỗ nào viết như ablation đã xong; mọi lần nhắc đều gắn nhãn Future Work tường minh. Không có vi phạm integrity.

### 3. Reproducibility & Experimental Rigor (20% weight)

- **Reproducibility:** **PASS (có điều kiện)** — §5 (dòng 123, đã verify) nói rõ pipeline được chạy độc lập 2 lần trên cùng seed, hai lần khớp nhau trong sai số dấu-phẩy-động/phiên bản thư viện thông thường. Sau sửa lỗi E, §6.3 giờ khoanh đúng phạm vi: claim reproducibility chỉ phủ data-split + tính PCA-residual, KHÔNG phủ tính ngẫu nhiên nội tại từng classifier hay việc pin phiên bản thư viện — đóng đúng khoảng cách giữa tên bài ("Reproducible...") và điều thực sự được đảm bảo.
- **Statistical rigor:** **FAIL dưới Q1** — một lần chia train/val/test duy nhất, không bootstrap, không khoảng tin cậy, không lặp lại nhiều seed (xác nhận trực tiếp câu cuối §6.3: "point estimates from a single held-out test split... we do not have the statistical evidence to state how much the ranking... would vary under resampling"). Đây là khoảng trống Q1 thật, không sửa được trong phạm vi bài này — nhưng được công khai trung thực, không che giấu.
- **Hyperparameter completeness:** **PASS-với-caveat** — §4.4 (dòng 111, đã verify) nói rõ cả 5 classifier dùng tham số mặc định của từng thư viện, "No venue-specific hyperparameter search was run for any of the five, which we treat as an explicit scope limitation rather than an oversight." Một reviewer Q1 vẫn sẽ đòi một ablation tuning/search — bài minh bạch không có, nhưng nêu đúng như một giới hạn phạm vi có chủ đích, không giấu diếm.

### 4. Theoretical / Mathematical Soundness (10% weight)

- **Proof gaps:** Không tìm thấy trong đối tượng hình thức duy nhất của bài — phương trình PCA-residual (§3, dòng 43-45). Verify bằng đại số trực tiếp: $R_i = \mu + \sum_{k=33}^{256} c_{i,k} u_k$ tương đương định nghĩa với $I_i - \sum_{k=1}^{32} c_{i,k} u_k$, vì $I_i = \mu + \sum_{k=1}^{256} c_{i,k} u_k$ (đẳng thức tái tạo PCA đầy đủ) — hai vế của phương trình trong bài nhất quán với nhau, không chỉ được khẳng định suông.
- **Notation issues:** Không phát hiện — $I$, $R$, $\mu$, $u_k$, $c_{i,k}$ đều được định nghĩa trước khi dùng (§3, dòng 39-49). Công thức bin-count LBP $P(P-1)+3=59$ cho $P=8$ đã kiểm tra độc lập bằng số học ($8\times7+3=59$, dòng 63) và khớp đúng công thức `nri_uniform` gốc của Ojala et al. [15].
- **Điểm mềm (không đủ nghiêm trọng để hạ verdict, nhưng đáng nêu):** bài không viết dạng đóng của toàn bộ feature map $\phi: R \mapsto \mathbb{R}^{187}$ thành một phương trình duy nhất — §4.2 định nghĩa từng descriptor riêng bằng văn xuôi. Tại venue Transaction-family Q1, một reviewer nhiều khả năng sẽ yêu cầu hình thức hóa; tại band Q4/Workshop đây là vấn đề trình bày, không phải đúng-sai.

### 5. Rejection Pattern Analysis

Khung Q1-giả định (theo đúng thang skill yêu cầu), mỗi mục đánh dấu trạng thái đã-sửa hay chưa-sửa-nhưng-đã-công-khai:

1. **I reject this claim because** §6.2 (bản gốc, trước sửa) khẳng định LightGBM giữ "best test F1" và "best test AUC" trong khi chính Table 1 của bài cho thấy XGBoost cao hơn ở cả hai cột đó — một reviewer Q1 đối chiếu bảng với văn bản luôn bắt được lỗi này, và nó phá vỡ lòng tin vào mọi số liệu khác trong bài. — **Trạng thái: ĐÃ SỬA** (dòng 145 + dòng 11 Abstract).
2. **I reject this claim because** §2 (bản gốc) đếm sai — "Two recent studies" trong khi liệt kê ba nghiên cứu — dấu hiệu bài chưa được đọc lại kỹ trước khi nộp. — **Trạng thái: ĐÃ SỬA** (dòng 31).
3. **I reject this claim because** §2 (bản gốc) rò rỉ thuật ngữ chấm điểm nội bộ "(T1)" và một cross-reference gãy tới Section 5 — Section 5 là Experimental Setup, không hề bàn novelty tier ở đâu cả. — **Trạng thái: ĐÃ SỬA** (dòng 35).
4. **I reject this claim because** §6.1 (bản gốc) tuyên bố một ngưỡng số học chính xác ("within 0.002 of AUC") mà chính Table 1 của bài vi phạm ở 3/5 classifier (gap thực tế 0.0023-0.0027) — một claim định lượng không sống sót nổi phép kiểm tra ngược lại chính bảng số của tác giả là mẫu hình desk-reject kinh điển ở Q1. — **Trạng thái: ĐÃ SỬA** (dòng 141, "roughly 0.003").
5. **I reject this claim because** tên bài có chữ "Reproducible" nhưng §5/§6.3 (bản gốc) chưa từng nói gì về tính ngẫu nhiên nội tại của 5 classifier hay việc pin phiên bản thư viện — một claim ở cấp tiêu đề rộng hơn phạm vi thực sự được đảm bảo bên trong bài. — **Trạng thái: ĐÃ SỬA** (câu mới, dòng 153).
6. **I reject this claim because** bài hoàn toàn không có ablation cấp thành phần (PCA-residual-vs-raw, hay leave-one-descriptor-out) — đây là lý do lớn nhất khiến một reviewer Q1 Transaction-family ra Major Reject bất kể mọi thứ khác trong bài tốt đến đâu. — **Trạng thái: KHÔNG SỬA ĐƯỢC TRONG PHẠM VI BÀI NÀY, nhưng đã công khai trung thực làm Future Work** (§6.3 dòng 153, §7 dòng 157) — không phải lỗi integrity, chỉ là giới hạn phạm vi T1 đã được ledger C-2 cho phép trước.
7. **I reject this claim because** Table 1 là ước lượng điểm từ một lần chia split duy nhất, không có bootstrap/CI/multi-seed — một reviewer Q1 sẽ hỏi liệu khoảng cách 0.002-0.003 AUC giữa các boosted tree có phân biệt được với nhiễu thống kê hay không, và bài tự thừa nhận không trả lời được câu đó. — **Trạng thái: KHÔNG SỬA ĐƯỢC TRONG PHẠM VI BÀI NÀY, đã công khai trung thực** (§6.3, câu cuối).

**Thất bại cụ thể dẫn tới desk-reject (nếu nộp thẳng vào venue Q1):**
- Thiếu ablation cấp thành phần hoàn toàn (mục 6).
- Không có kiểm định thống kê nào quanh bảng kết quả chính (mục 7).
- Không có baseline deep-learning được fine-tune trên đúng split này — số liệu [3]/[4]/[9] chỉ trích dẫn làm ngữ cảnh (§6.3, đã verify), không phải so sánh kiểm soát — một reviewer Q1 coi đây là so sánh thiếu, dù bài đã minh bạch nói rõ đây không phải so sánh trực tiếp.
- Tier T1 định nghĩa dưới trần Q1 theo chính rubric integrity — không phải điều bài có thể sửa bằng văn phong, chỉ có thể sửa bằng làm thêm thực nghiệm kiến trúc thật (con đường [6] đã tự nêu ở §7).

**Acceptance outlook:**
- **Theo chuẩn Q1:** Reject-likely. Ba lý do chặn lớn nhất: (1) tier T1 dưới trần Q1 theo rubric, không có ngoại lệ; (2) zero ablation cấp thành phần; (3) zero kiểm định thống kê quanh kết quả chính.
- **Theo venue band thật đã claim (Workshop/Q4/Scopus, claims-ledger C-1/C-2):** Competitive, với điều kiện 5 sửa đổi đã áp dụng trong chính lượt review này đứng vững qua một lượt kiểm tra chéo thật (đã thực hiện field-by-field so với Table 1/ledger/code ở trên) — không đưa ra tỷ lệ phần trăm vì không verify được.

### Hard Questions (must address)

1. **What is new here?** Không phải một descriptor mới hay một kiến trúc mới — là việc thay thế mô tả fractal đóng (FreeAeon FD/MFS/Lacunarity) của [1] bằng ba descriptor mở, tái lập được (FFT+LBP+noise-residual) trên đúng biểu diễn PCA-residual của [1], cộng với việc chạy classification thật (điều [1] chưa từng làm — [1] chỉ dừng ở kiểm định KS phân phối).
2. **Where is the ablation?** Chưa có. §6.3 (dòng 153) và §7 (dòng 157) nêu tường minh: so sánh PCA-residual-vs-raw-image bằng cùng bộ descriptor được xếp vào Future Work, chưa chạy, không claim là đã hoàn thành ở bất kỳ đâu trong bài.
3. **How does this differ from Yasir & Kim [4] at the component level?** [4] dùng HOG+LBP+KAZE trên ảnh gốc (raw); bài này dùng FFT+LBP+noise-residual trên ảnh đã qua PCA-residual (N=32, loại 32 thành phần chính). Khác cả bộ đặc trưng lẫn tầng tiền xử lý — khác biệt thật ở cấp thành phần, không phải đổi tên.
4. **Without the PCA-residual step, does the claim fall back to baseline?** Không biết — đây chính xác là ablation còn thiếu (câu hỏi 2). Bài không claim biết câu trả lời này, và không có chỗ nào ngầm giả định residual step là nguyên nhân của kết quả tốt mà chưa chứng minh.
5. **Is this reproducible by another team?** Có điều kiện. Data-split (seed=42) và phép tính PCA-residual per-ảnh là tái lập được chính xác. Tính ngẫu nhiên nội tại của 5 classifier (vd. bootstrap của RandomForest) và phiên bản thư viện không được pin/seed riêng — sau sửa lỗi E, bài giờ nói đúng điều này thay vì ngụ ý tái lập digit-for-digit.
6. **Why treat a boosted-tree gap of 0.002-0.003 AUC as a tie rather than a real ranking?** Vì khoảng cách đó nằm trong biên độ mà một seed khác hoặc một phiên bản thư viện khác hoàn toàn có thể xê dịch, và vì thứ hạng còn đảo ngược giữa validation (LightGBM thắng cả 3) và test (XGBoost thắng cả 3) — bài nêu rõ cả hai lý do này sau sửa lỗi A (dòng 145), không chỉ chọn một số đẹp hơn để tô hồng.

---

## Kết luận và bàn giao

**Verdict cuối:** PASS cho venue band thật đã claim (Workshop/hội nghị Q4/Scopus-index, `claims-ledger.md` C-1/C-2) — 5 lỗi phát hiện được (A-E) đều đã sửa trực tiếp vào `main.md` và verify lại bằng Read trong chính lượt review này, không còn lỗi integrity nào tồn đọng. Hai điểm yếu còn lại (ablation cấp thành phần, kiểm định thống kê) là giới hạn phạm vi đã được `claims-ledger.md` C-2 cho phép trước và được chính bài công khai trung thực làm Future Work — không phải vi phạm, không cần vòng FAIL→FIX tiếp theo.

**Disposition Q1-giả định (Major Reject) không mâu thuẫn với PASS ở trên** — đây là hai thước đo khác nhau theo đúng khung calibration đã nêu ở đầu báo cáo: rigor soi xét ở mức Q1, nhưng bar chấp nhận đúng bằng venue band thật.

**Bàn giao:** Task #22 (`self-evaluator`) — cổng cuối của pipeline `paper-writing-integrity.md` §6, đọc lại toàn bộ 5 báo cáo trước đó (`citation-guard`, `style-humanizer`, `latex-fix`, báo cáo này) cộng với `main.md` đã sửa, ra quyết định "done" cuối cùng.
