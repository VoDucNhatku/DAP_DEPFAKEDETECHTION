# Code dán vào Colab - Baseline "Raw" (không PCA-residual) cho ablation

## CẢNH BÁO QUAN TRỌNG - đọc trước khi copy

- MỖI ô code bên dưới là MỘT cell riêng trong Colab. Chỉ copy đúng phần nằm
  trong cặp dấu ```python và ```  - KHÔNG copy chữ giải thích tiếng Việt ở
  ngoài khối code (chính là lỗi bạn từng gặp: dán cả đoạn văn bản vào 1 cell
  Code làm SyntaxError vì ký tự `**`, `---` không phải Python hợp lệ).
- Mỗi cell dưới đây **tự chứa** (self-contained) - không còn phụ thuộc phải
  chạy đúng thứ tự cell cũ trong notebook gốc nữa, để tránh nhầm lẫn.
- Cell 1 có kiểm tra dữ liệu trước khi chạy. Nếu báo "KHONG TIM THAY ANH" thì
  dừng lại, chạy lại bước tải dữ liệu (cell mount Drive / gdown trong notebook
  gốc) rồi mới chạy lại Cell 1.

---

## Cell 1 - dán vào notebook `deepfake_pj_group_FEATURE.ipynb`, chạy ở một ô Code MỚI

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

feature_groups = {
    'fft': (0, FFT_BINS),
    'lbp': (FFT_BINS, FFT_BINS + LBP_BINS),
    'noise': (FFT_BINS + LBP_BINS, FEATURE_DIM),
}
feature_names = (
    [f'fft_{i}' for i in range(FFT_BINS)]
    + [f'lbp_{i}' for i in range(LBP_BINS)]
    + [f'noise_{i}' for i in range(NOISE_BINS)]
)

real_dir = os.path.join(DATA_DIR, 'real')
fake_dir = os.path.join(DATA_DIR, 'fake')
real_ok = os.path.isdir(real_dir) and len(os.listdir(real_dir)) > 0
fake_ok = os.path.isdir(fake_dir) and len(os.listdir(fake_dir)) > 0

if not (real_ok and fake_ok):
    print('KHONG TIM THAY ANH trong', DATA_DIR)
    print('real_dir ton tai:', os.path.isdir(real_dir), '| so file:', len(os.listdir(real_dir)) if os.path.isdir(real_dir) else 0)
    print('fake_dir ton tai:', os.path.isdir(fake_dir), '| so file:', len(os.listdir(fake_dir)) if os.path.isdir(fake_dir) else 0)
    print('=> Hay chay lai cac o Code tai du lieu (mount Drive / gdown, giai nen zip) trong notebook goc TRUOC, roi chay lai o nay.')
    raise SystemExit('Dung lai: chua co du lieu anh, xem thong bao phia tren.')

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
assert X_all_raw.shape[1] == FEATURE_DIM, 'Sai chieu dac trung: ' + str(X_all_raw.shape[1]) + ' != ' + str(FEATURE_DIM)
print('Tong (baseline raw):', len(y_all_raw), 'anh | real=' + str((y_all_raw == 0).sum()) + ' fake=' + str((y_all_raw == 1).sum()) + ' | dim=' + str(X_all_raw.shape[1]))
```

Ghi chú: các thông báo `print(...)` trong code cố tình viết không dấu (ASCII
thuần) — không phải vì tiếng Việt có dấu gây lỗi (Python 3 xử lý UTF-8 bình
thường), mà chỉ để bạn dễ đọc output ngay trong Colab mà không lo font/encoding
lạ trên một số máy. Phần giải thích quanh code (ngoài khối ```python```) mới
là phần có dấu đầy đủ để bạn đọc hiểu.

---

## Cell 2 - dán vào cell KẾ TIẾP trong cùng notebook `deepfake_pj_group_FEATURE.ipynb`

```python
import os
import pickle
import shutil
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

OUTPUT_DIR = '/content/features_baseline_raw'
os.makedirs(OUTPUT_DIR, exist_ok=True)

idx = np.arange(len(y_all_raw))
idx_train, idx_tmp = train_test_split(idx, test_size=0.2, stratify=y_all_raw, random_state=42)
idx_val, idx_test = train_test_split(idx_tmp, test_size=0.5, stratify=y_all_raw[idx_tmp], random_state=42)

scaler_raw = StandardScaler().fit(X_all_raw[idx_train])
config_raw = {
    'img_size': 256,
    'pca_remove': 0,
    'feature_dim': FEATURE_DIM,
    'lbp_method': 'nri_uniform',
    'split': '80/10/10',
    'note': 'baseline khong qua PCA-residual, dung de so sanh voi pipeline chinh',
}

for name, ids in [('train', idx_train), ('val', idx_val), ('test', idx_test)]:
    Xs = scaler_raw.transform(X_all_raw[ids]).astype(np.float32)
    ys = y_all_raw[ids]
    ps = [paths_all_raw[i] for i in ids]
    with open(OUTPUT_DIR + '/' + name + '_baseline_raw.pkl', 'wb') as f:
        pickle.dump({'X': Xs, 'y': ys, 'paths': ps, 'feature_names': feature_names, 'feature_groups': feature_groups, 'config': config_raw}, f)
    print(name, ':', len(ys), 'anh | shape=', Xs.shape, '->', name + '_baseline_raw.pkl')

with open(OUTPUT_DIR + '/scaler_baseline_raw.pkl', 'wb') as f:
    pickle.dump(scaler_raw, f)

DST = '/content/drive/MyDrive/Deepfake_project/features'
os.makedirs(DST, exist_ok=True)
for fname in ['train_baseline_raw.pkl', 'val_baseline_raw.pkl', 'test_baseline_raw.pkl', 'scaler_baseline_raw.pkl']:
    shutil.copy(OUTPUT_DIR + '/' + fname, DST + '/' + fname)
    print('Da luu len Drive:', fname)

print('XONG baseline raw. File nam canh file cu trong', DST)
```

Ghi chú thời gian chạy: vòng trích đặc trưng gốc (có PCA-residual) mất
khoảng 74 phút cho 40k ảnh (log thật trong notebook cũ: real 39:51 + fake
34:19). Baseline raw bỏ được bước `PCA().fit()/transform()/inverse_transform()`
cho từng ảnh nên sẽ nhanh hơn, nhưng chưa đo thời gian thực tế nên không ghi
số cụ thể ở đây.

---

## Cell 3 - dán vào notebook `model.ipynb`, THAY THẾ cho ô Code đang load
## `train.pkl/val.pkl/test.pkl` (không đổi cell train 5 classifier bên dưới nó)

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
print('Nhan - 0=Real, 1=Fake | Train:', np.bincount(y_train))
```

Sau khi chạy xong Cell 3, chạy tiếp nguyên văn ô Code định nghĩa 5 classifier
(`LinearRegression`, `RandomForest`, `XGBoost`, `LightGBM`, `CatBoost`) và
hàm `evaluate` đã có sẵn trong `model.ipynb` - KHÔNG cần sửa gì ở cell đó, vì
nó chỉ dùng lại biến `X_train/y_train/X_val/y_val/X_test/y_test` đã nạp ở
Cell 3.

---

## Nếu vẫn còn lỗi

Gửi nguyên văn dòng lỗi (bắt đầu từ `Traceback` hoặc dòng có chữ `Error`) -
không gửi lại mô tả bằng lời từ Colab tự động sinh ra, gửi log gốc để xác
định đúng nguyên nhân, tránh sửa sai chỗ.

## Việc cần gửi lại sau khi chạy xong

1. Bảng `df_results` cuối cùng (5 dòng model x 6 cột metric).
2. (Tùy chọn) thời gian chạy thực tế của Cell 1.

Sau khi có bảng, báo cáo so sánh sẽ được viết vào
`notes/experiment-ablation-pca-residual-vs-raw.md` theo đúng plan đã duyệt.
