# DAP_DEPFAKEDETECHTION

> Phát hiện ảnh deepfake dựa trên PCA Residual + Handcrafted Features (FFT/LBP/Noise) với 5 classifiers nhẹ (LightGBM tốt nhất: **Acc 86.6%, AUC 0.94**).<br>
> Mục tiêu nộp báo: **Q4 Workshop / Q3 Scopus Conference**. Novelt tier: **T1 - recipe** (closed-source tool replacement + classification evaluation bổ sung so với paper gốc).

---

## 📌 Abstract ngắn

Bài toán: phân biệt ảnh khuôn mặt thật vs ảnh sinh ra bởi AI генератор (deepfake).
Phương pháp: trích xuất residual image bằng PCA (zero-out top-32 components) → trích 187 handcrafted features (FFT 64 + LBP 59 + Noise 64) → 5 classifiers (LR / RF / XGBoost / LightGBM / CatBoost).
Thuộc tính explainable, lightweight (chạy trên CPU), không phải black-box CNN.

---

## 📂 Repo Organization

```text
├── Research-Deepfake/          # Bản gốc của paper lấy cảm hứng
│   ├── src/                    # Feature pipeline của paper gốc (FreeAeon - closed-source)
│   │   ├── feature.py          # ETL: PCA residual iteration + FreeAeon wrappers
│   │   ├── extract_feature.py  # Open-source replacement functions (FFT/LBP/Noise)
│   │   ├── common.py           # Visualization + baseline RandomForest
│   │   └── analyse.py / face_crop.py / face_resize.py
│   ├── install/
│   │   └── requirements.txt    # <-- FreeAeon-Fractal/FreeAeon-ML (cần license)
│   └── scripts/
│       └── pipline.sh
│
├── team-notebooks/             # Notebook pipeline của nhóm (đóng góp chính)
│   ├── deepfake_pj_group (2).ipynb        # Part A+B: download, face crop, feature extract
│   ├── deepfake_pj_group_FEATURE.ipynb    # Part A+B (variant): ablation 7 variants
│   └── model.ipynb                       # Part C: 5 classifiers → kết quả chính
│
├── notes/                      # Nghiên cứu / quản lý
│   ├── deepfake-status-report.md         # 📊 Tình trạng hiện tại, checklist, reviewer-rejection matrix
│   └── deepfake-action-plan.md           # 📋 Kế hoạch chi tiết 3 tuần, P0-P3 priority
│
├── install/
│   ├── requirements-paper.txt   # FreeAeon-Fractal/FreeAeon-ML (để chạy phần paper gốc)
│   └── requirements-open.txt    # Chỉ open-source (để chạy phần của nhóm)
│
└── README.md
```

---

## 🔽 Dữ liệu (không được commit — tuân thủ giấy phép của dataset gốc)

| Dataset | License / access | Kích thước (mình dùng) |
|---------|-----------------|----------------------|
| 1-million-fake-faces | Kaggle — không redistribute | ~1M fake (sample 10K) |
| Flickr Faces HQ (FFHQ) | NVIDIA public research license | ~10K real 256px |

Cả 2 đều lớn (multi-GB). Mình sẽ không chứa vào repo; xem hướng dẫn tải bên dưới. Nếu bạn có data đầy đủ, cấu trúc cần:

```text
Research-Deepfake/data/raw/1-million-fake-faces/   <- .jpg|.png
Research-Deepfake/data/raw/flickrfaceshq-dataset-ffhq/  <- .png
```

---

## ⚙️ Setup môi trường

### Prerequisites
- Python 3.10-3.11
- pip >= 24
- 8 GB RAM tối thiểu (16 GB để chạy end-to-end)
- GPU không bắt buộc (pipeline chạy trên CPU; thuần CPU xử lý ~50 ảnh/giây)

### Clone & dependency

```bash
git clone https://github.com/VoDucNhatku/DAP_DEPFAKEDETECHTION.git
cd DAP_DEPFAKEDETECHTION
```

| Environment | File | Mô tả |
|-------------|------|--------|
| Paper gốc | `install/requirements-paper.txt` | FreeAeon-Fractal + FreeAeon-ML |
| Team pipeline | `install/requirements-open.txt` | Chỉ open-source (không cần license) |

```bash
# Team reproducible source-only rebuild (open-source stack)
pip install -r install/requirements-open.txt

# Full paper gốc rebuild (require FreeAeon license)
pip install -r install/requirements-paper.txt
```

---

## 🔁 End-to-end Reproduction

Lưu ý quan trọng: **2 team-notebooks hiện không nhất quán về LBP method** (`uniform` ở notebook FEATURE, `nri_uniform` ở notebook (2)). Thứ tự này sẽ **bị fix sau** — trước khi tin vào bảng kết quả, chạy P0 pipeline để ensure shape 187 thống nhất.

### Pipeline overview

```text
raw/ (ảnh thật / ảnh fake từ Kaggle/NVIDIA)
   |  face_resize.py           -> 256x256 PNG (LANCZOS)
   |  face_crop.py            -> MTCNN crop
   v
PCA residual (per-image, zero-out top-32, inverse)
   |  team-notebooks/A+B      -> 187-dim (FFT 64 + LBP 59 + Noise 64)
   v
5 Classifiers (LR / RF / XGBoost / LightGBM / CatBoost)
   |  team-notebooks/C
   v
Results  -> notes/     -> status-report.md -> action-plan.md -> claims-ledger.md
```

Chạy bằng Jupyter:

```bash
jupyter notebook team-notebooks/deepfake_pj_group_FEATURE.ipynb
# -> train.pkl / val.pkl / test.pkl / scaler.pkl
jupyter notebook team-notebooks/model.ipynb
# -> model_results.csv + confusion matrices
```

Kết quả hiện tại (chờ re-run sau P0 fix):

| Model | Test Acc | F1 | AUC |
|-------|----------|-----|-----|
| LinearRegression | 0.8552 | 0.8574 | 0.9309 |
| RandomForest | 0.8350 | 0.8338 | 0.9144 |
| XGBoost | 0.8688 | 0.8687 | 0.9442 |
| LightGBM | 0.8662 | 0.8664 | 0.9427 |
| CatBoost | 0.8598 | 0.8594 | 0.9386 |

Mọi số báo cáo trong paper **phải match log file** — không được claim điều ngoài evidence.

---

## 🗺️ Roadmap (ưu tiên theo impact/effort)

Xem chi tiết tại `notes/deepfake-action-plan.md`, tóm tắt:

- **Tuần 1 — Must Have** (vé vào cửa, thiếu 1 cái bị loại):
  - P0: Unify LBP method, re-run pipeline, verify ablation 7 variants (~30 phút).
  - P2: SOTA baseline Xception / EfficientNet-B0 (~2 ngày).
  - P4: Related Work ≥ 10 papers (~2 buổi).
- **Tuần 2 — Should Have** (quyết định có hồn):
  - P3: Theoretical Bridge — FFT/LBP/Noise on residual là practical proxy cho Fractal descriptors.
- **Tuần 2 — Nice to Have** (điểm cộng):
  - P1: Robustness — bảng JPEG/blur/noise perturbations (~1 buổi).
- **Tuần 3:** Draft paper + Internal review + Polish + Submit.

---

## 🛡️ License

- **Nguồn gốc `Research-Deepfake/`**: thuộc về tác giả gốc (jim-xie-cn), phân phối theo giấy phép tương ứng `install/requirements.txt` (FreeAeon-Fractal 0.6.6 / FreeAeon-ML 0.3.7 là closed-source tools — cần license riêng để chạy).
- **Pipeline của nhóm (`team-notebooks/`) + paper sắp tới**: phát hành MIT License (`LICENSE.txt`) bởi DALIC — Deepfake Analysis & Learning Improvement Club, corresponding author Trieu Vy (`it.trieu.vy.27@gmail.com`).

Dataset không được repo này redistribute (kích thước lớn, license giới hạn). Dùng link tải chính chủ như đã liệt kê ở phần Dữ liệu.

---

## 🎯 Paper target & novelty grading

| Tier | Định nghĩa | Áp dụng cho bài này |
|------|-----------|---------------------|
| T1 — recipe | Đổi công cụ + thêm classification mà paper gốc không dùng | **Core contribution** |
| T2 — module | — | Không |
| T3 — reformulation | — | Không |

Target venue roadmap:
- **Q4 Workshop**: đủ với Must Have (P0 + P2 + P4).
- **Q3 Scopus Conference**: must-have + P3 (Theoretical Bridge).
- **Q1**: cần T2/T3 + 2+ datasets + extensive baselines — *không với scope hiện tại theo rubric research-proposal-integrity.md §1*.

---

## 🧭 Cách đóng góp

1. Commit đúng format Conventional Commits.
2. Mỗi commit dùng `Co-Authored-By: DALIC <it.trieu.vy.27@gmail.com>`.
3. Trước khi claim "đã chạy" — phải có log file.
4. Không force-push lên `main`; cần reviewer phê duyệt.

---

## 📩 Liên hệ

- Corresponding author: **Trieu Vy** — `it.trieu.vy.27@gmail.com`
- Organization: **DALIC** — Deepfake Analysis & Learning Improvement Club
- Repository maintainer: `VoDucNhatku` (GitHub)

---

## 📝 Trạng thái

| Checkpoint | Trạng | Ghi chú |
|---|---|---|
| Code chạy được | 🟡 Re-run sau P0 fix | `team-notebooks/` |
| Kết quả tái lập | 🟡 Chờ P0 (unify LBP) | `notes/` |
| Draft Paper | 🔴 Chưa bắt đầu | Tuần 3 |
| Claim governance | 🟡 Đang initialize | cần `notes/claims-ledger.md` |
