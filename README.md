# DAP_DEPFAKEDETECHTION

> Phát hiện ảnh khuôn mặt do AI sinh ra (AI-generated face detection), dựa trên đặc trưng
> thủ công mở (FFT + LBP + Noise-residual, 187 chiều) trích trên **ảnh dư PCA (PCA-residual)**,
> phân loại bằng 5 mô hình cổ điển (LinearRegression-ngưỡng, RandomForest, XGBoost, LightGBM,
> CatBoost). Đây là bản mở rộng có thể tái lập của công cụ đóng-nguồn (closed-source) FreeAeon
> trong bài báo gốc của Xie et al.
>
> **Bài báo đã viết xong bản thảo hoàn chỉnh** (`paper/main.md` / `paper/main.pdf`), đã qua đủ
> 6 khâu kiểm tra chất lượng nội bộ (xem [Trạng thái dự án](#-trạng-thái-dự-án)). Mọi con số
> trong README này lấy trực tiếp từ file kết quả đã verify — **không có số nào được suy đoán
> hay làm tròn tuỳ tiện**.

**Đọc file này xong là hiểu toàn bộ dự án — không cần tải gì thêm** ngoại trừ bộ dữ liệu ảnh
gốc (không thể redistribute trong repo vì lý do bản quyền, xem mục [Dữ liệu](#-dữ-liệu-không-commit-vào-repo)).
Toàn văn bài báo, mọi báo cáo kiểm tra, và toàn bộ ghi chú nghiên cứu đều nằm sẵn trong repo này.

---

## Mục lục

1. [Bài toán & phương pháp](#-bài-toán--phương-pháp)
2. [Kết quả chính](#-kết-quả-chính-đã-verify)
3. [Cấu trúc repo](#-cấu-trúc-repo)
4. [Dữ liệu (không commit vào repo)](#-dữ-liệu-không-commit-vào-repo)
5. [Cách chạy lại (reproduction)](#-cách-chạy-lại-reproduction)
6. [Novelty tier & venue mục tiêu](#-novelty-tier--venue-mục-tiêu)
7. [Trạng thái dự án](#-trạng-thái-dự-án)
8. [Việc còn tồn đọng / chưa làm](#-việc-còn-tồn-đọng--chưa-làm-nói-thẳng-không-giấu)
9. [License](#-license)
10. [Đóng góp & liên hệ](#-đóng-góp--liên-hệ)

---

## 📌 Bài toán & phương pháp

**Bài toán:** phân biệt nhị phân — ảnh khuôn mặt **thật** (real) vs ảnh khuôn mặt **do AI sinh
ra** (fake/AI-generated).

**Pipeline** (mô tả đầy đủ, có giải thích từng bước tại `paper/main.md` §4, Algorithm 1):

```text
Ảnh xám 256×256
   │
   ▼  PCA-residual (loại bỏ 32 thành phần chính đầu tiên, N=32 — kế thừa
   │  default của bài báo gốc Xie et al., KHÔNG phải kết quả sweep nội bộ)
   ▼
Ảnh dư PCA (PCA-residual image)
   │
   ▼  Trích đặc trưng thủ công, 187 chiều:
   │    • FFT magnitude-histogram — 64 bins
   │    • LBP histogram — 59 bins, method `nri_uniform`
   │      (chọn nri_uniform thay vì uniform vì P(P-1)+3 = 8×7+3 = 59 mã
   │       phân biệt cho P=8 neighbor, so với chỉ 10 mã nếu dùng uniform —
   │       dùng uniform ép về 59 bins sẽ làm ~83% bins luôn rỗng)
   │    • Noise-residual histogram (patch 8×8) — 64 bins
   ▼
StandardScaler → chia 80/10/10 (train/val/test), stratified, seed=42
   │
   ▼
5 classifier: LinearRegression (ngưỡng hoá), RandomForest, XGBoost,
              LightGBM, CatBoost
   ▼
Kết quả (bảng đầy đủ bên dưới)
```

Điểm khác với bài báo gốc: bài gốc (Xie et al., arXiv:2604.17268) chỉ dùng bộ công cụ **đóng
nguồn** FreeAeon-Fractal/FreeAeon-ML (FD/MFS/Lacunarity) và chỉ làm phân tích phân phối
(KS-test) — **không có bất kỳ thực nghiệm classification nào**. Đóng góp của dự án này (tier
**T1 — recipe**, xem mục Novelty bên dưới): thay bộ công cụ đóng bằng đặc trưng **mở, tái lập
được** (FFT/LBP/Noise — chỉ cần `numpy`/`scikit-image`/`opencv`) và **thêm thực nghiệm phân
loại thật** trên 5 classifier cổ điển.

Toàn văn phương pháp, công thức, và lý giải từng dòng Algorithm 1: xem **`paper/main.md`**
(Markdown, render công thức bằng KaTeX/MathJax) hoặc **`paper/main.pdf`** (bản PDF đã biên dịch
qua XeLaTeX, giữ nguyên định dạng nộp bài).

---

## 📊 Kết quả chính (đã verify)

Bảng dưới đây **khớp 100%** với Table 1 trong `paper/main.md` (đã đối chiếu độc lập 2 lần —
xem `paper/reports/self-evaluator.md` mục "Chi tiết mục 6"). Dữ liệu: 40.000 ảnh (20.000 ảnh
thật từ FFHQ + 20.000 ảnh fake từ bộ "1 Million Fake Faces"), chia 80/10/10 = 32.000/4.000/4.000
ảnh, `random_state=42`.

| Model | Val Acc | Val F1 | Val AUC | Test Acc | Test F1 | Test AUC |
|---|---|---|---|---|---|---|
| LinearRegression (ngưỡng) | 0.8535 | 0.8556 | 0.9321 | 0.8552 | 0.8574 | 0.9309 |
| RandomForest | 0.8355 | 0.8346 | 0.9121 | 0.8350 | 0.8338 | 0.9144 |
| **XGBoost** | 0.8680 | 0.8685 | 0.9415 | **0.8688** | **0.8687** | **0.9442** |
| LightGBM | **0.8690** | **0.8700** | **0.9424** | 0.8662 | 0.8664 | 0.9427 |
| CatBoost | 0.8602 | 0.8608 | 0.9360 | 0.8598 | 0.8594 | 0.9386 |

**Đọc đúng bảng này** (điểm từng bị viết sai ở một bản nháp báo cáo trước đây trong dự án,
đã sửa — xem `paper/reports/ieee-q1-devil-advocate.md` mục sửa lỗi B): trên **tập validation**,
**LightGBM** đạt điểm cao nhất cả 3 chỉ số. Nhưng trên **tập test** (chỉ số quyết định cuối
cùng) thì **XGBoost thắng cả 3 chỉ số** (Acc/F1/AUC), LightGBM về nhì sát nút. Bài báo báo cáo
trung thực cả hai, không chỉ tô hồng một mô hình.

---

## 📂 Cấu trúc repo

```text
DAP_DEPFAKEDETECHTION/
├── paper/                          # ★ Bài báo hoàn chỉnh — đọc cái này trước tiên
│   ├── main.md                     #   Bản thảo đầy đủ (Markdown, 194 dòng)
│   ├── main.pdf                    #   Bản PDF đã biên dịch (XeLaTeX, 11 trang)
│   ├── main.tex                    #   Nguồn LaTeX dùng để biên dịch main.pdf
│   └── reports/                    #   5 báo cáo kiểm tra chất lượng (xem mục Trạng thái)
│       ├── citation-guard.md
│       ├── style-humanizer.md
│       ├── latex-fix.md
│       ├── ieee-q1-devil-advocate.md
│       └── self-evaluator.md
│
├── team-notebooks/                 # Notebook thật đã chạy trên Google Colab (đóng góp chính)
│   ├── deepfake_pj_group_FEATURE.ipynb  # Trích đặc trưng: PCA-residual + FFT/LBP/Noise
│   ├── deepfake_pj_group (2).ipynb      # Tải dữ liệu + face-crop (MTCNN) + biến thể trích đặc trưng
│   └── model.ipynb                      # Train + đánh giá 5 classifier -> bảng kết quả ở trên
│
├── Research-Deepfake/               # Bản sao nguyên vẹn của repo GỐC (KHÔNG sửa đổi)
│   │                                 # Nguồn: https://github.com/jim-xie-cn/Research-Deepfake
│   │                                 # Đi kèm bài báo: "Fractal Characterization of
│   │                                 # Low-Correlation Signals in AI-Generated Image
│   │                                 # Detection" (Xie et al., arXiv:2604.17268)
│   ├── src/                         # Code gốc: PCA-residual + FreeAeon FD/MFS/Lacunarity (đóng nguồn)
│   ├── install/requirements.txt     # Cần license FreeAeon-Fractal/FreeAeon-ML để chạy đủ
│   └── README.md                    # README gốc của tác giả jim-xie-cn
│
├── src/                             # Bản làm việc — hiện GIỐNG HỆT Research-Deepfake/src/
│   │                                 # (đã diff xác nhận không lệch), giữ ở top-level để
│   │                                 # team-notebooks/ import theo đường dẫn tương đối cũ.
│   ├── feature.py, extract_feature.py, common.py, analyse.py, face_crop.py, face_resize.py
│   └── mtcnn/
│
├── notes/                           # Toàn bộ ghi chú nghiên cứu, có provenance rõ ràng
│   ├── claims-ledger.md             # ★ Sổ ghi novelty tier + venue claim (C-1, C-2) — nguồn xác thực duy nhất cho mọi khẳng định về venue
│   ├── related-work-papers.md       # 6 nguồn Related Work vòng 2 (đã verify thủ công qua WebFetch)
│   ├── synthesize-gaps-deepfake-pca-residual.md   # 8 nguồn nền (S1–S8) + phân tích khoảng trống nghiên cứu
│   ├── deepfake-status-report.md    # Báo cáo tình trạng kỹ thuật chi tiết (đọc code trực tiếp)
│   ├── deepfake-action-plan.md      # Kế hoạch hành động P0–P3 (một phần đã hoàn thành trong paper)
│   ├── review-deepfake-status-report.md   # Review độc lập của status-report ở trên
│   ├── guide-a-to-z-baseline-to-paper.md  # Hướng dẫn chạy thực nghiệm ablation PCA-residual-vs-Raw
│   ├── colab-cells-baseline-raw-ablation.md  # Code cell dán trực tiếp vào Colab cho ablation trên
│   ├── LAM-THEO-DAY-DU.md           # Bản rút gọn, làm-theo-từng-bước của hướng dẫn ablation trên
│   └── archive/                     # Artifact của vòng verify tài liệu ĐẦU TIÊN — ĐÃ BỊ THAY THẾ,
│       │                             # giữ lại chỉ để minh bạch quá trình, KHÔNG dùng làm nguồn
│       └── related-work-papers-ROUND1-SUPERSEDED-2026-07-08.md  (+ log quá trình phát hiện lỗi)
│
├── scripts/
│   ├── download_papers.py           # Script tải + verify paper Related Work (đã sửa 2 bug sau vòng 1)
│   ├── pipline.sh / kill.sh / start-jupyter.sh
│
├── install/
│   ├── requirements-paper.txt       # Để chạy phần paper gốc (cần FreeAeon license)
│   └── requirements-open.txt        # Chỉ open-source (để chạy phần của nhóm)
│
├── data/                            # Rỗng trong repo (gitignore) — xem mục Dữ liệu
├── papers/                          # PDF nguồn tham khảo tải về cục bộ (gitignore, không commit)
└── LICENSE.txt                      # MIT (chi tiết ở mục License bên dưới)
```

---

## 🔽 Dữ liệu (không commit vào repo)

| Dataset | Vai trò | License / nguồn tải |
|---|---|---|
| Flickr Faces HQ (FFHQ) | 20.000 ảnh **thật** | NVIDIA public research license — [github.com/NVlabs/ffhq-dataset](https://github.com/NVlabs/ffhq-dataset) |
| "1 Million Fake Faces" (StyleGAN) | 20.000 ảnh **fake** | Kaggle, tác giả `tunguz` — không redistribute — [kaggle.com/datasets/tunguz/1-million-fake-faces](https://www.kaggle.com/datasets/tunguz/1-million-fake-faces) |

Tổng cộng dùng **40.000 ảnh** (20.000 real + 20.000 fake) — đây là con số thật đã dùng để ra
Table 1 ở trên, khác với các bản ghi chú/README cũ trong lịch sử dự án có ghi số ước lượng
nhỏ hơn (đã sửa ở đây cho khớp với số liệu paper thật).

Cả hai bộ đều lớn (nhiều GB) và có điều khoản license không cho phép redistribute — **repo
này không chứa ảnh gốc**. Muốn chạy lại từ đầu, tự tải theo 2 link trên rồi đặt vào:

```text
data/raw/1-million-fake-faces/          <- .jpg | .png
data/raw/flickrfaceshq-dataset-ffhq/    <- .png
```

---

## ⚙️ Cách chạy lại (reproduction)

### Yêu cầu
- Python 3.10–3.11, pip ≥ 24
- 8 GB RAM tối thiểu (khuyến nghị 16 GB cho pipeline full)
- Không bắt buộc GPU — toàn bộ pipeline chạy được trên CPU (nhóm chạy thật trên Google Colab)

### Cài đặt

```bash
git clone https://github.com/VoDucNhatku/DAP_DEPFAKEDETECHTION.git
cd DAP_DEPFAKEDETECHTION

# Chỉ cần phần open-source (đủ để chạy team-notebooks/)
pip install -r install/requirements-open.txt

# Muốn chạy thêm phần paper gốc (FreeAeon FD/MFS/Lacunarity) — cần license riêng
pip install -r install/requirements-paper.txt
```

### Chạy pipeline (đã chạy thật trên Google Colab, không phải giả định)

```bash
jupyter notebook team-notebooks/deepfake_pj_group_FEATURE.ipynb
# -> train.pkl / val.pkl / test.pkl / scaler.pkl (187-dim, PCA-residual N=32, LBP nri_uniform)

jupyter notebook team-notebooks/model.ipynb
# -> bảng kết quả 5 classifier, khớp với Table 1 ở mục Kết quả chính
```

Mọi số liệu báo cáo trong `paper/main.md` truy được về đúng notebook trên (không có số nào
được viết mà không có nguồn — nguyên tắc xuyên suốt dự án).

### (Chưa chạy) Thí nghiệm ablation PCA-residual vs Raw

Có sẵn hướng dẫn từng bước + code dán trực tiếp vào Colab tại
`notes/guide-a-to-z-baseline-to-paper.md` + `notes/colab-cells-baseline-raw-ablation.md`
(bản rút gọn: `notes/LAM-THEO-DAY-DU.md`) để so sánh: đặc trưng thủ công trích trên ảnh
PCA-residual có tốt hơn trích trên **ảnh gốc (raw, không qua PCA)** hay không. **Đây là thí
nghiệm CHƯA CHẠY** — hướng dẫn đã sẵn sàng nhưng chưa có kết quả thật nào được ghi nhận. Bài
báo hiện tại (`paper/main.md` §6.3) nêu rõ đây là giới hạn/future work, không claim đã có kết
quả ablation này.

---

## 🎯 Novelty tier & venue mục tiêu

Nguồn xác thực duy nhất: **`notes/claims-ledger.md`** (mọi thay đổi về claim đều được ghi lại
ở đây theo nguyên tắc "không recalibrate ngầm" — thay đổi phải trích dẫn claim cũ + lý do).

| Mục | Giá trị | Ghi chú |
|---|---|---|
| Novelty tier | **T1 — recipe** | Thay công cụ đóng nguồn (FreeAeon) bằng đặc trưng mở + thêm classification thật — không phải kiến trúc/module mới (T2), không phải tái định nghĩa bài toán (T3) |
| Venue band | **Workshop / hội nghị Q4 / Scopus-index** | **Tuyệt đối không phải Q1** một mình theo rubric tại `~/.claude/rules/research-proposal-integrity.md` §1 — T1 không đủ điều kiện Q1 dù có bao nhiêu kết quả tốt |
| Điều kiện nâng band | Cần ablation-với-classifier + SOTA deep-learning baseline + ≥2 dataset | Cả 3 điều kiện này **hiện chưa đạt** — xem mục "Việc còn tồn đọng" |

Bản thảo đã qua phản biện đối kháng kiểu Q1 IEEE (`paper/reports/ieee-q1-devil-advocate.md`)
— verdict: **PASS cho venue band thật** (Workshop/Q4/Scopus), *không* PASS chuẩn Q1 (đúng như
kỳ vọng cho một đóng góp tier T1).

---

## 📝 Trạng thái dự án

Toàn bộ pipeline viết bài báo (`~/.claude/rules/paper-writing-integrity.md` §6) đã chạy đủ
**6/6 khâu, tất cả PASS**:

| # | Khâu | Verdict | Báo cáo |
|---|---|---|---|
| 1 | Soạn bản thảo (`paper-submission`) | ✅ Hoàn tất — 194 dòng | `paper/main.md` |
| 2 | Kiểm tra trích dẫn (`citation-guard`) | ✅ PASS — 17/17 nguồn verify DOI/arXiv thật, 0 trích dẫn mồ côi | `paper/reports/citation-guard.md` |
| 3 | Hiệu chỉnh văn phong (`style-humanizer`) | ✅ PASS — giữ nguyên 100% số liệu/công thức | `paper/reports/style-humanizer.md` |
| 4 | Sửa & biên dịch LaTeX (`latex-fix` + XeLaTeX) | ✅ PASS — biên dịch thành công `paper/main.pdf`, 11 trang | `paper/reports/latex-fix.md` |
| 5 | Phản biện đối kháng (`ieee-q1-devil-advocate`) | ✅ PASS cho venue band thật; phát hiện và sửa 5 lỗi thật ngay trong lượt review | `paper/reports/ieee-q1-devil-advocate.md` |
| 6 | Đánh giá cuối (`self-evaluator`) | ✅ PASS — đối chiếu độc lập 9 hạng mục, chỉ 2 issue mức Low (không chặn) | `paper/reports/self-evaluator.md` |

**Kết luận:** bản thảo đã sẵn sàng cho venue mục tiêu thật (Workshop/hội nghị Q4/Scopus-index).
Trước khi nộp thật, nhóm chỉ còn 2 việc hành chính (không phải nội dung học thuật):

1. Điền tên tác giả thật + khoa/trường + email liên hệ thật (hiện là placeholder
   `[Author name — nhóm điền]` trong `paper/main.md`/`paper/main.pdf`, theo đúng nguyên tắc
   "không bịa tên" khi chưa biết tên thật).
2. (Tuỳ chọn) áp bảng ánh xạ đánh số lại References theo appearance-order nếu venue đích yêu
   cầu nghiêm ngặt — bảng ánh xạ sẵn sàng tại `paper/reports/citation-guard.md` §3.1.

---

## 🔴 Việc còn tồn đọng / chưa làm (nói thẳng, không giấu)

- **Ablation PCA-residual vs Raw image**: hướng dẫn + code đã viết sẵn (mục Reproduction ở
  trên) nhưng **chưa chạy trên Colab**, chưa có kết quả thật. Không phải blocker cho venue
  band hiện tại (Workshop/Q4/Scopus) — bài đã nêu rõ đây là limitation.
- **Không có SOTA deep-learning baseline** (Xception/EfficientNet fine-tune trên đúng split
  này) — chỉ trích dẫn số liệu từ các bài khác làm ngữ cảnh liên hệ, không phải so sánh kiểm
  soát trực tiếp (bài đã nói rõ điều này ở §6.3, không che giấu).
  Đây cũng là lý do venue band bị chặn ở Q4/Scopus chứ không lên được cao hơn.
- **Không robustness test** (JPEG/blur/noise/resize trên ảnh test) — nêu trong Future Work,
  chưa chạy.
- **Không sweep đa mức N** cho PCA-residual — N=32 kế thừa nguyên default của bài báo gốc, chưa
  tự làm sensitivity analysis nội bộ.
- **Tên tác giả thật chưa điền** vào bản thảo (xem mục Trạng thái ở trên).
- Thư mục `src/` (top-level) hiện là **bản sao giống hệt** `Research-Deepfake/src/` — chưa dọn
  gộp lại thành một nguồn duy nhất (giữ nguyên hiện trạng để không phá import path của
  `team-notebooks/`, nhưng đây là trùng lặp cần dọn nếu có thời gian).

---

## 🛡️ License

- **`Research-Deepfake/`** (bản sao nguyên vẹn code gốc): thuộc bản quyền tác giả gốc
  **jim-xie-cn** — [github.com/jim-xie-cn/Research-Deepfake](https://github.com/jim-xie-cn/Research-Deepfake).
  Phần dùng công cụ **FreeAeon-Fractal 0.6.6 / FreeAeon-ML 0.3.7** trong đó là **đóng nguồn**,
  cần license riêng để chạy (`Research-Deepfake/install/requirements.txt`).
- **Phần đóng góp của nhóm** (`team-notebooks/`, `paper/`, `notes/`, `src/` bản làm việc): phát
  hành theo **MIT License** — xem toàn văn tại [`LICENSE.txt`](LICENSE.txt). Bản quyền:
  **DALIC — Deepfake Analysis & Learning Improvement Club**, corresponding author **Trieu Vy**
  (`it.trieu.vy.27@gmail.com`), theo đúng nội dung ghi trong `LICENSE.txt`.
- **Dữ liệu** (FFHQ, 1-million-fake-faces): không thuộc bản quyền của dự án này, không được
  redistribute — xem mục [Dữ liệu](#-dữ-liệu-không-commit-vào-repo).

---

## 🧭 Đóng góp & liên hệ

**Quy ước commit:**
1. Theo định dạng [Conventional Commits](https://www.conventionalcommits.org/).
2. Trước khi claim "đã chạy" trong commit message hoặc note — phải có log/output thật kèm
   theo (nguyên tắc "tuyệt đối không bịa" xuyên suốt dự án).
3. Không force-push lên `main`.

**Liên hệ:**
- Corresponding author (theo `LICENSE.txt`): **Trieu Vy** — `it.trieu.vy.27@gmail.com`
- Tổ chức: **DALIC** — Deepfake Analysis & Learning Improvement Club
- Repository maintainer (GitHub): [`VoDucNhatku`](https://github.com/VoDucNhatku)
- Repo: [github.com/VoDucNhatku/DAP_DEPFAKEDETECHTION](https://github.com/VoDucNhatku/DAP_DEPFAKEDETECHTION)
