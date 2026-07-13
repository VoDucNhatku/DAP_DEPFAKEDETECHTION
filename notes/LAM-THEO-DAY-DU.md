# Làm theo đúng thứ tự, từ trên xuống dưới. Không cần mở file nào khác.

Bạn đang có sẵn tab Colab đang chạy — dùng đúng tab đó, không cần upload gì
mới.

---

## Bước 1 — Mở notebook trích đặc trưng

Trên Colab, mở đúng notebook đang có tên `deepfake_pj_group_FEATURE.ipynb`
(tab bạn đang chạy).

## Bước 2 — Tạo 1 ô Code mới, dán đoạn này vào, bấm Shift+Enter

```python
import os
import numpy as np
import cv2
from tqdm import tqdm
from skimage.feature import local_binary_pattern

DATA_DIR = '/content/project_data'
LBP_P, LBP_R = 8, 1
FFT_BINS = 64
LBP_BINS = LBP_P * (LBP_P - 1) + 3
NOISE_BINS = 64
FEATURE_DIM = FFT_BINS + LBP_BINS + NOISE_BINS

def extract_fft(gray):
    f = np.fft.fftshift(np.fft.fft2(gray.astype(np.float32)))
    mag = np.log1p(np.abs(f))
    hist, _ = np.histogram(mag, bins=FFT_BINS, range=(mag.min(), mag.max()))
    return hist.astype(np.float32) / (hist.sum() + 1e-8)

def extract_lbp(gray):
    lbp = local_binary_pattern(gray, P=LBP_P, R=LBP_R, method='nri_uniform')
    hist, _ = np.histogram(lbp.ravel(), bins=LBP_BINS, range=(0, LBP_BINS))
    return hist.astype(np.float32) / (hist.sum() + 1e-8)

def extract_noise(gray):
    noise = gray.astype(np.float32) - cv2.GaussianBlur(gray, (5, 5), 0).astype(np.float32)
    hist, _ = np.histogram(noise, bins=NOISE_BINS, range=(-50, 50))
    return hist.astype(np.float32) / (hist.sum() + 1e-8)

def extract_features(gray):
    return np.concatenate([extract_fft(gray), extract_lbp(gray), extract_noise(gray)])

feature_groups = {'fft': (0, FFT_BINS), 'lbp': (FFT_BINS, FFT_BINS + LBP_BINS), 'noise': (FFT_BINS + LBP_BINS, FEATURE_DIM)}
feature_names = [f'fft_{i}' for i in range(FFT_BINS)] + [f'lbp_{i}' for i in range(LBP_BINS)] + [f'noise_{i}' for i in range(NOISE_BINS)]

real_dir = os.path.join(DATA_DIR, 'real')
fake_dir = os.path.join(DATA_DIR, 'fake')
real_ok = os.path.isdir(real_dir) and len(os.listdir(real_dir)) > 0
fake_ok = os.path.isdir(fake_dir) and len(os.listdir(fake_dir)) > 0

if not (real_ok and fake_ok):
    print('KHONG TIM THAY ANH trong', DATA_DIR, '- chay lai buoc tai du lieu o dau notebook truoc.')
    raise SystemExit('Dung lai.')

X_all_raw, y_all_raw, paths_all_raw = [], [], []
for label_name, label_idx in [('real', 0), ('fake', 1)]:
    folder = os.path.join(DATA_DIR, label_name)
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    print('[BASELINE-RAW]', label_name.upper(), len(files), 'anh')
    for fname in tqdm(files, desc='baseline_raw_' + label_name):
        img = cv2.imread(os.path.join(folder, fname), cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        img = cv2.resize(img, (256, 256))
        X_all_raw.append(extract_features(img))
        y_all_raw.append(label_idx)
        paths_all_raw.append(os.path.join(folder, fname))

X_all_raw = np.asarray(X_all_raw, dtype=np.float32)
y_all_raw = np.asarray(y_all_raw, dtype=np.int32)
print('Tong (baseline raw):', len(y_all_raw), 'anh | dim=', X_all_raw.shape[1])
```

**Xong bước 2 khi thấy:** dòng cuối `Tong (baseline raw): 40000 anh | dim= 187`.
Nếu thấy `KHONG TIM THAY ANH` thì dừng, nhắn cho tôi.

## Bước 3 — Tạo tiếp 1 ô Code mới (vẫn trong notebook FEATURE), dán đoạn này, chạy

```python
import os, pickle, shutil
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

OUTPUT_DIR = '/content/features_baseline_raw'
os.makedirs(OUTPUT_DIR, exist_ok=True)

idx = np.arange(len(y_all_raw))
idx_train, idx_tmp = train_test_split(idx, test_size=0.2, stratify=y_all_raw, random_state=42)
idx_val, idx_test = train_test_split(idx_tmp, test_size=0.5, stratify=y_all_raw[idx_tmp], random_state=42)

scaler_raw = StandardScaler().fit(X_all_raw[idx_train])

for name, ids in [('train', idx_train), ('val', idx_val), ('test', idx_test)]:
    Xs = scaler_raw.transform(X_all_raw[ids]).astype(np.float32)
    ys = y_all_raw[ids]
    ps = [paths_all_raw[i] for i in ids]
    with open(OUTPUT_DIR + '/' + name + '_baseline_raw.pkl', 'wb') as f:
        pickle.dump({'X': Xs, 'y': ys, 'paths': ps, 'feature_names': feature_names, 'feature_groups': feature_groups}, f)
    print(name, ':', len(ys), 'anh ->', name + '_baseline_raw.pkl')

with open(OUTPUT_DIR + '/scaler_baseline_raw.pkl', 'wb') as f:
    pickle.dump(scaler_raw, f)

DST = '/content/drive/MyDrive/Deepfake_project/features'
os.makedirs(DST, exist_ok=True)
for fname in ['train_baseline_raw.pkl', 'val_baseline_raw.pkl', 'test_baseline_raw.pkl', 'scaler_baseline_raw.pkl']:
    shutil.copy(OUTPUT_DIR + '/' + fname, DST + '/' + fname)

print('XONG buoc 3.')
```

**Xong bước 3 khi thấy:** dòng cuối `XONG buoc 3.`

## Bước 4 — Chuyển sang notebook `model.ipynb`

Mở tab/notebook `model.ipynb`. Tìm ô Code đang load `train.pkl`/`val.pkl`/
`test.pkl` (thường ngay sau ô mount Drive) — **xoá nội dung ô đó, thay bằng
đoạn dưới đây**, rồi chạy:

```python
import pickle
import numpy as np

PKL_DIR = '/content/drive/MyDrive/Deepfake_project/features/'

with open(PKL_DIR + 'train_baseline_raw.pkl', 'rb') as f:
    train_data = pickle.load(f)
with open(PKL_DIR + 'val_baseline_raw.pkl', 'rb') as f:
    val_data = pickle.load(f)
with open(PKL_DIR + 'test_baseline_raw.pkl', 'rb') as f:
    test_data = pickle.load(f)

X_train, y_train = train_data['X'], train_data['y']
X_val, y_val = val_data['X'], val_data['y']
X_test, y_test = test_data['X'], test_data['y']

print('[BASELINE RAW] Train:', X_train.shape, 'Val:', X_val.shape, 'Test:', X_test.shape)
```

## Bước 5 — Chạy tiếp các ô Code còn lại trong `model.ipynb` như bình thường

Không sửa gì thêm — cứ chạy lần lượt các ô có sẵn (định nghĩa 5 model +
huấn luyện + in bảng kết quả), y như bạn vẫn làm trước giờ.

## Bước 6 — Gửi lại cho tôi

Copy nguyên bảng kết quả cuối cùng (5 dòng model, có Accuracy/F1/AUC) dán
vào chat. Xong.

---

Nếu ở bước nào báo lỗi: chụp màn hình hoặc copy nguyên dòng đỏ báo lỗi, gửi
cho tôi, không cần tự sửa.
