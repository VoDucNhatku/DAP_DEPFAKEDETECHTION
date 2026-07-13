# Hướng dẫn A-Z: chạy baseline -> viết báo cáo Q4

- Phạm vi: từ bước chạy thí nghiệm baseline (PCA-residual vs Raw) đến khi có
  bản thảo bài báo Q4 hoàn chỉnh.
- Người thực hiện: gobal-orchestrator (không dùng sub-agent, theo yêu cầu
  phiên làm việc).
- Ngày: 2026-07-13.
- Liên quan: `notes/claims-ledger.md` (C-1), `notes/synthesize-gaps-deepfake-pca-residual.md`.

---

## Cách mở các file local được nhắc trong hướng dẫn này

Tất cả đường dẫn bên dưới là đường dẫn THẬT trên máy bạn (đã kiểm tra tồn tại
trước khi viết vào file này, không đoán). Mở bằng File Explorer (dán đường
dẫn vào thanh địa chỉ) hoặc bằng VS Code / Notepad.

| File | Đường dẫn đầy đủ | Dùng để làm gì |
|---|---|---|
| Code để dán vào Colab | `D:\CPV-VIP\DAP_DEPFAKEDETECHTION\notes\colab-cells-baseline-raw-ablation.md` | Mở file này, copy từng ô code (Cell 1/2/3) sang Colab |
| Notebook trích đặc trưng | `D:\CPV-VIP\DAP_DEPFAKEDETECHTION\team-notebooks\deepfake_pj_group_FEATURE.ipynb` | Nơi dán Cell 1 và Cell 2 |
| Notebook train model | `D:\CPV-VIP\DAP_DEPFAKEDETECHTION\team-notebooks\model.ipynb` | Nơi dán Cell 3 |
| Nguồn Related Work đã verify (14 nguồn) | `D:\CPV-VIP\notes\related-work-papers.md` | Dùng khi viết phần Related Work, KHÔNG dùng bản 50 nguồn suy đoán |
| Ledger novelty/venue | `D:\CPV-VIP\notes\claims-ledger.md` | Nơi ghi lại mọi claim, sẽ cập nhật sau khi có kết quả thật |

**Về link Colab:** bạn đã có sẵn tab Colab đang chạy (vì bạn vừa báo lỗi từ
đó) — tôi KHÔNG biết URL Google Drive/Colab riêng của bạn nên không thể đưa
link bấm-là-mở được. Bạn chỉ cần mở lại đúng tab Colab đó và file local ở
trên trong 2 cửa sổ cạnh nhau để copy qua.

Nếu bạn chưa có tab Colab nào đang mở: vào `https://colab.research.google.com`
-> chọn tab "Upload" -> chọn đúng file `deepfake_pj_group_FEATURE.ipynb` từ
đường dẫn ở bảng trên.

---

## Toàn bộ công đoạn từ giờ đến khi có bài báo (tổng quan trước, chi tiết ở dưới)

```
[1] Chạy Cell 1+2 (trích đặc trưng baseline raw)    <- BẠN làm trên Colab
[2] Chạy Cell 3 + train 5 classifier                <- BẠN làm trên Colab
[3] Bạn gửi lại bảng kết quả cho tôi                 <- BẠN gửi
[4] Tôi verify số liệu + viết báo cáo ablation       <- TÔI làm
[5] Tôi cập nhật claims-ledger.md                    <- TÔI làm
[6] Tôi soạn khung bài báo Q4 đầy đủ                 <- TÔI làm
[7] (tùy thời gian) robustness test cơ bản           <- BẠN chạy + TÔI viết
[8] Tự-kiểm-tra cuối cùng trước khi gọi là xong       <- TÔI làm, bắt buộc
```

---

## [1] Chạy Cell 1 + Cell 2 trên Colab (notebook FEATURE)

1. Mở `deepfake_pj_group_FEATURE.ipynb` trên Colab (tab đang chạy hoặc upload
   như hướng dẫn ở trên).
2. **Kiểm tra trước khi chạy gì mới:** chạy lại (hoặc xác nhận đã chạy) các ô
   Code gốc phần tải dữ liệu (mount Drive / gdown / giải nén zip) ở ĐẦU
   notebook. Sau khi chạy xong ô đó, phải thấy dòng in ra dạng:
   `[THANH CONG] Real: 20000 anh | Fake: 20000 anh`
   Nếu KHÔNG thấy dòng này hoặc số khác 20000/20000 -> dừng lại, không chạy
   Cell 1 bên dưới, báo cho tôi biết số thực tế bạn thấy.
3. Bấm nút `+ Code` để tạo 1 ô Code mới (đặt sau các ô gốc).
4. Mở file local `colab-cells-baseline-raw-ablation.md` (đường dẫn ở bảng
   trên), tìm phần **Cell 1** (nằm giữa cặp dấu ```` ```python ```` và
   ```` ``` ````), copy CHÍNH XÁC từ dòng `import os` đến hết dòng cuối
   `print('Tong (baseline raw): ...`. KHÔNG copy chữ tiếng Việt phía ngoài
   khối code.
5. Dán vào ô Code vừa tạo, bấm Shift+Enter để chạy.
6. **Kiểm tra kết quả Cell 1 (bắt buộc, không bỏ qua):**
   - Nếu thấy dòng `KHONG TIM THAY ANH` -> dừng lại, quay về bước 2.
   - Nếu chạy bình thường: sẽ thấy 2 thanh tiến trình (tqdm) cho `real` và
     `fake`, mỗi thanh chạy đến 20000/20000 (có thể mất 30-70 phút tùy tốc
     độ GPU/CPU Colab đang cấp, chưa có số chính xác vì chưa đo thật).
   - Dòng cuối cùng phải là: `Tong (baseline raw): 40000 anh | real=20000
     fake=20000 | dim=187`. Nếu số khác 40000/20000/20000/187 -> dừng lại,
     copy nguyên văn dòng lỗi/output gửi cho tôi.
7. Tạo ô Code mới tiếp theo, copy **Cell 2** từ file local, dán vào, chạy.
8. **Kiểm tra kết quả Cell 2:** phải thấy 3 dòng dạng
   `train : 32000 anh | shape= (32000, 187) -> train_baseline_raw.pkl`
   (và tương tự cho `val`/`test` với 4000 ảnh mỗi tập), rồi đến dòng
   `Da luu len Drive: train_baseline_raw.pkl` (x4 lần cho 4 file), và dòng
   cuối `XONG baseline raw. File nam canh file cu trong ...`. Nếu thiếu bất
   kỳ dòng nào trong số này -> dừng lại, gửi lỗi cho tôi.

## [2] Chạy Cell 3 + classifier trên Colab (notebook model.ipynb)

1. Mở `model.ipynb` trên Colab.
2. Tìm ô Code đang load `train.pkl`/`val.pkl`/`test.pkl` (ở đầu notebook, sau
   phần mount Drive) - **thay thế** ô đó bằng **Cell 3** trong file local
   (không xóa ô mount Drive phía trước nó, chỉ thay ô load file).
3. Chạy ô vừa thay.
4. **Kiểm tra:** phải thấy dòng `[BASELINE RAW] Train: (32000, 187) Val:
   (4000, 187) Test: (4000, 187)`. Nếu báo lỗi không tìm thấy file
   `train_baseline_raw.pkl` -> nghĩa là bước [1] chưa lưu lên Drive thành
   công, quay lại kiểm tra lại bước [1] mục 8.
5. Chạy tiếp NGUYÊN VĂN ô Code định nghĩa 5 model (`LinearRegression`,
   `RandomForest`, `XGBoost`, `LightGBM`, `CatBoost`) và vòng lặp `evaluate`
   đã có sẵn trong `model.ipynb` - không sửa gì ở đây.
6. **Kiểm tra kết quả cuối cùng:** phải thấy bảng `TONG KET CAC MO HINH` in
   ra 5 dòng (1 dòng/model) x 6 cột (`Val Acc, Val F1, Val AUC, Test Acc,
   Test F1, Test AUC`). Đây chính là bảng cần gửi lại ở bước [3].

## [3] Gửi lại kết quả cho tôi

Copy nguyên văn bảng `TONG KET CAC MO HINH` (dạng text, hoặc chụp màn hình
nếu tiện hơn) và dán vào chat. Kèm theo (nếu có) thời gian chạy thực tế của
Cell 1.

## [4] Tôi verify + viết báo cáo ablation (tôi làm, sau khi nhận được số ở bước 3)

- Đối chiếu bảng số mới (baseline raw) với bảng số cũ (PCA-residual, đã có
  sẵn trong `model.ipynb` hiện tại: LightGBM Test Acc 0.8662 / AUC 0.9427,
  XGBoost 0.8688/0.9442, CatBoost 0.8598/0.9386, RandomForest 0.8350/0.9144,
  LinearRegression-threshold 0.8552/0.9309).
- Viết file `notes/experiment-ablation-pca-residual-vs-raw.md`: bảng so
  sánh 2 cột (PCA-residual vs Raw) x 5 model, diễn giải trung thực đúng 1
  trong 2 kịch bản đã nói rõ trong plan (PCA-residual thắng rõ / không thắng
  rõ) - không overclaim theo hướng nào cả, chỉ báo đúng số thật.
- KHÔNG viết bất kỳ con số nào vào file này nếu chưa nhận được từ bạn ở bước
  [3] - đây là nguyên tắc "tuyệt đối không bịa" xuyên suốt phiên làm việc.

## [5] Cập nhật claims-ledger.md

Thêm 1 dòng mới vào `notes/claims-ledger.md` (không sửa dòng C-1 cũ) ghi rõ:
đã chạy thực nghiệm ablation PCA-residual-vs-raw, kết quả ra sao, có ảnh
hưởng gì đến downgrade trigger của C-1 hay không (downgrade trigger của C-1
là về sweep-N/KS-correlation, khác với ablation này, nhưng nếu ablation cho
thấy PCA-residual KHÔNG giúp ích thì phải ghi rõ vào ledger vì nó làm yếu đi
một phần luận điểm của bài).

## [6] Soạn khung bài báo Q4 đầy đủ

Theo đúng pipeline chuẩn trong `~/.claude/rules/paper-writing-integrity.md`
mục 6 (rule này đang binding cho cả phiên làm việc):

```
paper-submission draft/format   (soạn Abstract, Method, Baseline&Ablation,
                                  Results, Related Work, Limitation)
        |
        v
citation-guard        - kiểm tra không trích dẫn bịa, DOI của 14 nguồn
                         Related Work đã verify thật sự tồn tại
        |
        v
style-humanizer       - chuẩn hóa văn phong, KHÔNG đổi số liệu/claim strength
        |
        v
latex-fix + compile   - đảm bảo công thức (nếu có) render đúng cả KaTeX
                         (VS Code) và MathJax (GitHub)
        |
        v
ieee-q1-devil-advocate - phản biện đối kháng, chấm lại novelty tier so với
                          claims-ledger.md (không được vượt T1 đã chốt)
        |
        v
self-evaluator         - công đoạn cuối trước khi gọi là "xong"
```

Mỗi công đoạn viết báo cáo riêng cạnh bản thảo (`paper/reports/<stage>.md`) -
nếu 1 công đoạn FAIL thì quay lại công đoạn sinh ra lỗi trước khi đi tiếp,
không bỏ qua.

## [7] (tùy thời gian còn lại) Robustness test cơ bản

Nếu còn thời gian sau khi có bài báo nháp: biến đổi ảnh trong test set hiện
có (nén JPEG q=50, resize 50%, làm mờ sigma=2, thêm nhiễu Gaussian N(0,10)),
infer lại bằng model ĐÃ TRAIN (không train lại), so sánh accuracy trước/sau
biến đổi. Đây là thí nghiệm rẻ (không cần GPU nặng, không cần dữ liệu mới).

## [8] Tự-kiểm-tra cuối cùng trước khi báo "xong" (bắt buộc, tôi làm)

Trước khi báo cáo bất kỳ kết quả nào là hoàn tất, tôi sẽ:
1. Đối chiếu lại mọi con số trong báo cáo với output thật bạn gửi (không
   dùng từ trí nhớ hội thoại).
2. Quét lại file báo cáo + `claims-ledger.md` theo đúng cách
   `hallucination-guard` mode `scan` đã làm ở bước trước trong phiên này
   (mọi claim phải có nguồn: file path / dòng output cụ thể).
3. Nếu phát hiện claim nào thiếu nguồn -> dừng lại, ghi rõ "chưa xác minh",
   không tự suy diễn để lấp đầy.

---

## Nếu kết quả không như mong đợi (PCA-residual không thắng Raw)

Đây VẪN LÀ kết quả hợp lệ cho bài Q4 - không phải thất bại. Phải viết trung
thực thành "quan sát kiểm soát: trong thiết lập này, PCA-residual không cho
lợi thế rõ rệt so với đặc trưng thô trên ảnh gốc" - dùng ở phần Discussion/
Limitation, không che giấu, không sửa số để ép ra kết luận mong muốn. Đây là
nguyên tắc "tuyệt đối không bịa" đã được nhắc lại xuyên suốt phiên làm việc.
