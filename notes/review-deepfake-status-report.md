# Review: deepfake-status-report.md — độ chính xác & thay đổi kế hoạch

- Target: `DAP_DEPFAKEDETECHTION/notes/deepfake-status-report.md` (349 dòng; **IDENTICAL** với bản `D:\CPV-VIP\notes\deepfake-status-report.md` — đã `diff`, không lệch byte nào)
- Worker: gobal-orchestrator (inline, không sub-agent)
- Date: 2026-07-09
- Method: Grep trực tiếp trên 2 notebook nguồn (line-level) + WebSearch xác minh venue + Read/diff toàn bộ `notes/` ở cả 2 thư mục + Read 2 file log tải bài báo mới phát hiện

---

## Câu hỏi 1: "Có chuẩn xác chưa?"

### Phần ĐÚNG, đã corroborate độc lập (giữ nguyên, không cần sửa)
- Section 2 (novelty tier T1, venue band Workshop/Q4/Q3-Scopus, không Q1) — khớp 100% với `claims-ledger.md` dòng C-1, tự suy ra độc lập bằng rubric `research-proposal-integrity.md` §1, không phải trùng hợp.
- Section 3.1/3.3/3.4 (inventory hiện trạng code, dataset, split) — khớp với code đã grep trực tiếp.
- Section 6 (timeline), Section 7 (checklist), Section 8 (Q&A) — không phát hiện sai lệch.

### Phần SAI, xếp theo mức độ nghiêm trọng

**[NGHIÊM TRỌNG NHẤT — phát hiện mới, ngoài phạm vi câu hỏi gốc nhưng bắt buộc phải báo]**
Status-report Section 3.2/4 nói Related Work "🔴 Chưa có" (P4). Thực tế phức tạp hơn nhiều và nguy hiểm hơn "chưa có":

1. `DAP_DEPFAKEDETECHTION/notes/related-work-papers.md` (32KB, 50 candidate, "curated 20", ký tên "Trieu Vy (team)", 2026-07-08) đã tồn tại sẵn — **khác hoàn toàn** với file cùng tên tôi tạo ở `D:\CPV-VIP\notes\related-work-papers.md` (đã `diff` xác nhận khác). Tuyệt đại đa số 50 mục mang tag `[unverified]`, tên tác giả kiểu "Multiple groups", "[various]", "or similar", năm kiểu "2009 or 2014" — đúng pattern hallucination-guard cảnh báo ("Confident guess... say không biết, cần kiểm tra"), không phải citation thật.
2. Team đã cố tự động tải/verify qua 2 pipeline — `downloaded_papers_status.md` (Semantic Scholar, hầu hết "Not Found") và `downloaded_papers_status_openalex.md` (OpenAlex, một số "Already Downloaded"). Tôi đọc trực tiếp file OpenAlex và phát hiện **các cặp title↔filename bị lệch hoàn toàn miền chủ đề** — bằng chứng cụ thể (đọc trực tiếp, độ tin cậy cao, không suy diễn):
   - Dòng 8: title claim "*An Overview of ML/DL/RL... in Quantitative Finance*" (bài về **tài chính định lượng**) nhưng file tải về tên là `[10]_..._Arif_Fractal_Dimension-Based_Detection_of_Dee...pdf` (bài về **fractal dimension deepfake**) — 2 chủ đề không liên quan.
   - Dòng 13: title claim "*Brain tumor detection and classification using ML: a comprehensive survey*" (**y ảnh não**) nhưng filename là `[11]_..._Dou_Fractal_and_Multi-fractal_Analysis_for_I...pdf` (**fractal ảnh**).
   - Dòng 17: title claim "*A survey on Image Data Augmentation for Deep Learning*" nhưng filename là `[18]_..._Chalapathy_PCA-based_Anomaly_Detection...pdf`.
   - Dòng 28: title claim "*Convolutional Neural Networks: A Survey*" nhưng filename là `[41]_..._Hybrid_Deepfake_Detection_using_Statisti...pdf`.
   - Dòng 10: title claim "*Digital Image Watermarking Techniques: A Review*" nhưng filename là `[7]_..._Mahdian_Fractal-Based_Detection_of_Digital_Image...pdf`.

   Kết luận: pipeline tự động (rất có thể search bằng title đã hallucinate ở bước trước → search engine trả về kết quả gần đúng chữ nhất, sai hoàn toàn về nội dung) đã **gán nhầm PDF cho nhãn**. Nếu team cite những dòng này "as-is", team sẽ trích dẫn sai bài — rủi ro academic integrity nghiêm trọng hơn cả "chưa làm Related Work".
3. Tôi cũng spot-check 2 title khả nghi nhất bằng WebSearch trực tiếp phiên này ("Frequency and Spatial Domain Features... XGBoost (XGBF)", "Detecting AI-generated Images Using PCA Reconstruction Error") — **không tìm thấy bài nào khớp chính xác tên đó**, chỉ có bài liên quan chủ đề nhưng tên khác. Không đủ để khẳng định 100% là bịa (chưa check hết 50 mục), nhưng củng cố thêm nghi vấn ở mức medium-high.
4. Trong khi đó, bộ 14 nguồn ĐÃ verify thật của tôi (`D:\CPV-VIP\notes\related-work-papers.md` 6 bài vòng 2 + 8 bài trong `synthesize-gaps-deepfake-pca-residual.md`, mỗi bài đã WebFetch xác nhận tồn tại + đúng tên tác giả/venue) **chỉ nằm ở `D:\CPV-VIP\notes\`**, KHÔNG có bản sao trong `DAP_DEPFAKEDETECHTION\notes\` — cùng với `claims-ledger.md`. Team làm việc từ folder project có thể không biết các file này tồn tại.

**[NGHIÊM TRỌNG — đã nêu trong task gốc, tái xác minh trực tiếp bằng grep lần này]**
LBP method bị gán ngược notebook + khuyến nghị sai kỹ thuật, ở cả `deepfake-status-report.md` (dòng 78-80, 216, 323) **và** `deepfake-action-plan.md` (dòng 23-24, đã confirm 2 file này IDENTICAL giữa 2 thư mục nên lỗi tồn tại ở cả 4 chỗ):
- Report nói: FEATURE.ipynb dùng `uniform`, `(2).ipynb` dùng `nri_uniform`, khuyến nghị chọn `uniform`.
- Grep trực tiếp cho kết quả **ngược lại**: `deepfake_pj_group (2).ipynb:298` → `method='uniform'`, `bins=59` cứng (dòng 287); `deepfake_pj_group_FEATURE.ipynb:296` → `method='nri_uniform'`, `LBP_BINS = LBP_P*(LBP_P-1)+3 = 59` tính động (dòng 285).
- Về kỹ thuật: `nri_uniform` với P=8 sinh đúng 59 mã — khớp hoàn hảo với 59 bin. `uniform` với P=8 chỉ sinh P+2 = 10 mã — bị nhồi vào 59 bin, khiến 49/59 bin (~83% khối LBP, ~26% cả vector 187 chiều) luôn bằng 0 (cột chết). **Khuyến nghị đúng phải là `nri_uniform`, không phải `uniform`.**

**[TRUNG BÌNH]**
- "ViTsing Workshop" (dòng 314, bảng venue §9) — WebSearch phiên này (`"ViTsing" workshop CVPR ICCV ECCV computer vision`) **0 kết quả liên quan**. Không xác minh được đây là venue thật — nghi là lỗi chính tả hoặc tên bịa, phải gắn cờ `[chưa xác minh]`, không được đưa thẳng vào kế hoạch chính thức.
- Dòng 317: "CVPR/ICCV/ECCV workshop... dễ hơn" — khung diễn đạt này đáng ngờ, các track workshop tại top-tier venue vẫn cạnh tranh cao, không nên set kỳ vọng sai cho bài T1.

**[NHỎ]**
- Dòng 24: typo "research-proposal-integracy" → đúng phải là `research-proposal-integrity.md`.
- Dòng 313 (bảng §9, hàng ICIP/ICPR/WACV): cột "Phù hợp?" ghi ❌ nhưng nội dung mô tả lại nêu điều kiện có thể đạt được — logic mâu thuẫn, nên sửa thành 🟡 (có điều kiện) thay vì ❌.

---

## Câu hỏi 2: "Có thay đổi gì với kế hoạch hiện tại không?"

1. **Sửa hướng LBP ở cả 4 vị trí** (status-report dòng 78-80/216/323 + action-plan dòng 23-24, cả 2 thư mục vì file identical): đổi khuyến nghị từ `uniform` → `nri_uniform`; sửa lại gán notebook đúng chiều. Bản kỹ thuật chi tiết đã có sẵn ở `D:\CPV-VIP\notes\synthesize-gaps-deepfake-pca-residual.md` (mục "Xử lý bug LBP").
2. **Dừng dùng `DAP_DEPFAKEDETECHTION/notes/related-work-papers.md` (50-candidate) làm nguồn trích dẫn as-is** — không phải vì "chưa xong" mà vì có bằng chứng cụ thể về sai lệch PDF↔nhãn. Team nên: (a) dùng bộ 14 nguồn đã verify của tôi (`D:\CPV-VIP\notes\related-work-papers.md` + `synthesize-gaps-...md`) làm nền, hoặc (b) nếu muốn giữ 50-candidate, phải verify lại TỪNG mục qua Crossref/arXiv DOI trực tiếp (không qua pipeline tự động title-matching như đã dùng) trước khi cite bất kỳ dòng nào.
3. **Đồng bộ 2 thư mục notes/** — hiện `claims-ledger.md` và `synthesize-gaps-deepfake-pca-residual.md` chỉ tồn tại ở `D:\CPV-VIP\notes\`, không có ở `DAP_DEPFAKEDETECHTION\notes\` nơi team thực sự làm việc. Cần copy hoặc trỏ team sang đọc ở root để tránh lạc thông tin.
4. **Gắn cờ "ViTsing Workshop"** là chưa xác minh được, không đưa vào bản kế hoạch chính thức cho đến khi tìm ra tên venue thật; đồng thời làm mềm câu "CVPR/ICCV/ECCV workshop dễ hơn".
5. Sửa 2 lỗi nhỏ (typo, logic bảng §9).

## Chưa làm (đợi xác nhận)
Chưa chỉnh sửa trực tiếp file `deepfake-status-report.md` / `deepfake-action-plan.md` / `related-work-papers.md` ở project — chỉ báo cáo phát hiện theo đúng pattern đã dùng trong phiên này (hỏi trước khi sửa file kế hoạch của user).

---

## Addendum (2026-07-09, phiên sau) — Root cause đã trace, verify lại bằng code + đọc nội dung PDF thật

User tự trace ra root cause ở `scripts/download_papers.py`. Đã đọc toàn bộ file (182 dòng) + đọc trực tiếp nội dung 2 PDF nghi vấn để verify — không suy luận suông.

### Đúng (2/3 điểm)
1. **`query_openalex()` (dòng 57-69) trả `data['results'][0]` không verify** author/year/domain — đúng, đọc thấy nguyên văn, không có bước so khớp nào.
2. **`parse_markdown()` (dòng 44-45) skip entry có author "various/multiple/[group]/unknown" bằng `continue`** — đúng, đây là lý do report chỉ có ~30/50 dòng thay vì 50.

### SAI 1 điểm quan trọng — "file đúng bài, chỉ title bị đè nhầm"
Đọc code dòng 125-134 cho thấy: `pdf_url` lấy từ `oa_data['open_access']['oa_url']` — **`oa_data` chính là candidate[0] bị mismatch**, không có nguồn "metadata gốc" nào khác (hàm `parse_markdown` **không hề trích DOI/URL** từ `related-work-papers.md` — chỉ có id/title/authors/year). Chỉ riêng **filename** là build từ title gốc; **nội dung PDF tải về cũng từ candidate[0] sai luôn**.

Verify bằng cách đọc trực tiếp nội dung file `papers/[11]_2022_Dou_Fractal_and_Multi-fractal_Analysis_for_I.pdf` — **nội dung thật là bài "Brain tumor detection and classification using machine learning: a comprehensive survey" (Amin et al., Complex & Intelligent Systems 2022, DOI 10.1007/s40747-021-00563-y)** — hoàn toàn là bài y ảnh não, không liên quan fractal/deepfake dù filename ghi vậy. → Kết luận: **file PDF tải về cũng sai nội dung, không chỉ sai title hiển thị trong báo cáo.**

### Lỗi thứ 3 — chưa được nhắc: `download_pdf()` không check content-type
Dòng 91 có comment "*We don't strictly check content type anymore to catch more files*" — hệ quả: nhiều "PDF" thực chất là trang HTML bot-verification (Cloudflare/Akamai) bị lưu nhầm đuôi `.pdf`. Quét magic-byte (`%PDF`) toàn bộ `papers/` (20 file): **8/20 (40%) không phải PDF thật** — ví dụ `[10]_..._Arif_Fractal_Dimension....pdf` thực chất là trang HTML redirect chứa `bm-verify=...` (bot challenge page), không mở được.

### Tổng kết mức độ rủi ro thực tế (sửa lại so với hypothesis gốc)
Không phải "title sai, file đúng" mà là 3 tầng lỗi chồng nhau, tệ hơn:
- ~40% file trong `papers/` không phải PDF thật (HTML bot-page).
- Trong số còn lại là PDF thật, ít nhất 1 case verify trực tiếp là **nội dung hoàn toàn sai chủ đề** (y học não thay vì deepfake) — do cùng cơ chế candidate[0] không verify.
- Report table hiển thị title sai (đã nêu ở review gốc) — hệ quả cùng gốc.

## Xử lý đề xuất
1. **Không dùng bất kỳ file nào trong `DAP_DEPFAKEDETECHTION/papers/` để cite hoặc đọc as-is** cho tới khi verify lại — kể cả file "Success"/"Already Downloaded".
2. **Quét toàn bộ `papers/` bằng magic-byte** (`head -c4` == `%PDF`) → xoá/cách ly ngay các file HTML giả dạng `.pdf` (8 file đã xác định).
3. Với 12 file còn lại (PDF thật): **verify tay từng file** — mở trang đầu, so title/author thật với dòng tương ứng trong `related-work-papers.md`; giữ lại nếu khớp, loại nếu không (như case [11] vừa xác nhận sai).
4. **Fix script trước khi chạy lại** (nếu muốn dùng tiếp pipeline này): (a) sau khi lấy `candidate[0]`, so khớp tên tác giả/năm với entry gốc (fuzzy match ngưỡng tối thiểu) trước khi accept, reject nếu lệch; (b) `download_pdf()` phải check `response.headers.get('content-type')` chứa `application/pdf` HOẶC check 4 byte đầu `%PDF` trước khi ghi file, reject nếu không khớp; (c) không skip âm thầm bằng `continue` — log rõ những entry bị skip ra file riêng để review được đầy đủ 50/50 thay vì mất dấu ~20 dòng.
5. **Khuyến nghị thực tế nhất**: nguồn gốc (`related-work-papers.md` 50-candidate) đã tự nó phần lớn `[unverified]`/hedge-worded — sửa script cũng không giải quyết gốc rễ là garbage-in. Nên bỏ pipeline tự động này, dùng bộ 14 nguồn đã verify tay (`D:\CPV-VIP\notes\related-work-papers.md` + `synthesize-gaps-deepfake-pca-residual.md`) làm nền Related Work — tất cả đã WebFetch xác nhận tồn tại thật, đúng tên tác giả/venue.

## Thuật ngữ (Glossary)
| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| metadata mismatch | lệch metadata | Tên bài báo và nội dung PDF tải về không khớp nhau |
| citation hallucination | trích dẫn bịa | Citation nghe hợp lý nhưng không verify được tồn tại thật |

---

## Addendum (2026-07-09, cùng phiên) — Đã fix `download_papers.py`, kết quả thực nghiệm

Theo yêu cầu "fix cho tôi đi thật chi tiết" — đã sửa trực tiếp
`DAP_DEPFAKEDETECHTION/scripts/download_papers.py` (182 dòng gốc → viết lại toàn bộ),
chạy lại 3 lần cho tới khi hết bug, verify từng bước bằng cách đọc nội dung PDF thật
chứ không chỉ tin log của chính script.

### Các thay đổi trong script

1. **Tách title khỏi phần "Author et al., Year, Venue" bị dính chung dòng** (Bug A,
   phần gốc) — regex 2 bước strip glued-suffix trước khi query, thay vì gửi cả chuỗi
   thô cho OpenAlex.
2. **Đổi endpoint OpenAlex** từ `search=` (full-text relevance, dễ trôi chủ đề) sang
   `filter=title.search:<title>` (chỉ khớp field title) + lấy 3 candidate thay vì tin
   mù `candidate[0]`.
3. **`pick_best_candidate()` — 3 lớp verify trước khi accept**, không có lớp nào thì
   reject (không âm thầm nhận bừa):
   - title similarity (`difflib.SequenceMatcher`) ≥ 0.45
   - year lệch ≤ 1 (nếu biết year)
   - **author cross-check** (lớp mới phát hiện cần thiết giữa chừng — xem "Bug tự bắt
     được" bên dưới): so surname trong `related-work-papers.md` với `authorships` thật
     của candidate trên OpenAlex, reject nếu không khớp tên nào.
4. **`download_pdf()` giờ đọc full response rồi kiểm tra 4 byte đầu `== %PDF`** trước
   khi ghi đĩa (Bug B, phần gốc) — không còn ghi HTML bot-page nhầm đuôi `.pdf`.
5. **Không còn `continue` âm thầm** — entry bị skip (author field "various/multiple/
   group/unknown") giờ ghi ra `notes/related-work-skipped-unverifiable.md` kèm lý do.

### Bug tự bắt được giữa chừng (đáng nói vì đúng loại lỗi user lo ngại lặp lại)

Lần chạy đầu tiên (chỉ có title+year check, chưa có author check): entry **[22]**
("CNN-generated Images Are Surprisingly Easy to Spot...", author ghi trong file là
**Durall, Keuper, Schall**) được accept với title_sim=0.93 và tải về thành công
(qua được check `%PDF`). Không dừng ở "tải thành công" — đọc thẳng trang 1 của PDF vừa
tải: tác giả thật là **Sheng-Yu Wang, Oliver Wang, Richard Zhang, Andrew Owens, Alexei
A. Efros** (arXiv:1912.11035, CVPR 2020) — trùng title (2 bài khác nhau cùng chủ đề
frequency-artifact GAN detection hay bị nhầm với nhau trong literature) nhưng **hoàn
toàn khác tác giả**. Đây chính là dạng lỗi gốc (title khớp, nội dung sai) tái diễn dưới
hình thức khác — title-similarity một mình không đủ.

→ Thêm bước 3 ở trên (author cross-check qua OpenAlex `authorships`), sửa 1 bug phụ
trong regex tách surname (`\bet al\.?\b` bị backtrack bỏ sót dấu `.` treo lại, làm
"Rössler et al." so sánh trật với "Andreas Rössler" — sửa bằng cách bỏ `\b` cuối), rồi
chạy lại lần 3 mới ổn định.

### Kết quả thực nghiệm cuối cùng (lần chạy thứ 3, sạch)

| Chỉ số | Trước fix (log cũ) | Sau fix |
|---|---|---|
| Tổng candidate parse được | 50 (ước tính, không log skip) | 27 |
| Skip vì author không xác định | không log (âm thầm mất) | 23 (log đủ trong `related-work-skipped-unverifiable.md`) |
| Accept (qua hết 3 lớp verify) | ~50 (mù, không verify) | **1** |
| Reject (Not Found / title-sim thấp / year lệch / author lệch) | 0 (không có khái niệm reject) | 26 |
| File PDF thật tải về | ước tính 12/20 (60%, magic-byte scan) | **1/1 (100%), verify %PDF + nội dung khớp tác giả thật** |

Bài duy nhất pass hết 3 lớp verify: **[1] FaceForensics++ (Rössler et al. 2019)** —
title_sim=1.00, author khớp (Andreas Rössler có trong authorships thật trên OpenAlex),
file tải về có header `%PDF` hợp lệ, dung lượng 7.3MB — file thật, không phải trang
bot-challenge.

**Đọc đúng con số 1/27 accept:** đây KHÔNG phải nghĩa là "chỉ có 1 bài trong 50 candidate
là thật" — nó nghĩa là chỉ có 1 bài **OpenAlex tìm thấy dưới đúng cách diễn đạt title
trong `related-work-papers.md` VÀ tác giả khớp**. Phần lớn 26 "Not Found/Rejected" là vì
file nguồn `related-work-papers.md` vốn đã là danh sách 50 candidate phần lớn
`[unverified]`/hedge-worded (author ghi kiểu "Mahdian, Saic (2009) or Ghosh, Bora
(2014)", "Various groups", "or similar, 2020-2021"...) — bản thân nó chưa phải một
citation list đã confirm tồn tại thật, không phải lỗi của script. Đây là bằng chứng
thêm củng cố khuyến nghị #5 ở review gốc bên trên: **nên dùng bộ 14 nguồn đã verify tay
ở `D:\CPV-VIP\notes\related-work-papers.md`** làm nền Related Work, không nên tiếp tục
đổ công sức verify từng dòng trong 50-candidate list này.

### Dọn dẹp `papers/` (an toàn, không xoá gì)

- 20 file cũ (8 HTML giả + 12 PDF, trong đó có ít nhất [11] xác nhận sai nội dung) đã
  di chuyển (không xoá) vào
  `DAP_DEPFAKEDETECHTION/papers/_quarantine_pre_fix_2026-07-09/`.
- Report cũ `downloaded_papers_status_openalex.md` đã backup thành
  `downloaded_papers_status_openalex.md.pre_fix_backup_2026-07-09` trước khi bị ghi đè.
- `papers/` hiện tại chỉ còn đúng 1 file, đã verify: `[1]_2019_R_ssler_FaceForensics_Learning_to_Detect_Mani.pdf`.

### File đã tạo/sửa trong addendum này

- **Sửa:** `DAP_DEPFAKEDETECHTION/scripts/download_papers.py` (viết lại toàn bộ)
- **Ghi mới:** `DAP_DEPFAKEDETECHTION/notes/related-work-skipped-unverifiable.md` (23 dòng skip có lý do)
- **Ghi đè (có backup):** `DAP_DEPFAKEDETECHTION/notes/downloaded_papers_status_openalex.md`
- **Quarantine (không xoá):** `DAP_DEPFAKEDETECHTION/papers/_quarantine_pre_fix_2026-07-09/` (20 file cũ)

### Việc chưa làm, cần user quyết định

- **Chưa** đổi format `related-work-papers.md` sang multi-line thống nhất (đây là lựa
  chọn (b) từng nêu trong review gốc) — script hiện đã tự xử lý được cả 2 format lẫn
  lộn nên việc này không còn bắt buộc để đúng, chỉ còn là dọn dẹp thẩm mỹ. Không làm
  trừ khi được yêu cầu.
- **Chưa** verify tay 12 file PDF thật còn lại trong quarantine (ngoài [11] đã xác nhận
  sai) — nếu cần dùng lại bất kỳ file nào trong quarantine, phải verify tay từng file
  trước, không tin filename.
