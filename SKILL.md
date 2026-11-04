---
name: event-kit
description: 活動招生套組。辦講座、分享會、說明會時，一次做出整套招生素材：直式海報（含報名 QR code）、一頁式報名網頁（Vercel 免費架站）、Google 報名表單＋名單試算表、網頁報名直接寫進試算表、短影音背景簡報（每主題標題頁＋6 重點頁，字可改的 PPT＋PDF）。當使用者說「辦講座」「辦分享會」「做活動海報」「做報名頁」「做報名表單」「報名名單」「短影音背景簡報」「每個主題做一頁簡報」時觸發，也可以只做其中一項。預設繁體中文（台灣用語）。
---

# event-kit：活動招生套組

範例全部來自「小室房屋 11/17 房東出租全攻略分享會」（見 `references/內容範例.md`）。
開工前先讀 `references/踩坑紀錄.md`——裡面每一條都是實際踩過的。

## 產出清單

| # | 產出 | 工具 |
|---|---|---|
| 1 | 直式海報 1080×1920（講師照淡出、6 主題、資訊欄、報名 QR） | `templates/poster.html` → `scripts/render.sh` |
| 2 | Google 報名表單＋名單試算表（海報圖＋活動介紹） | `scripts/google-form.gs` |
| 3 | 一頁式報名網頁，送出直接進同一份試算表 | `templates/landing.html` → Vercel |
| 4 | 報名 QR code | `scripts/make_qr.py` |
| 5 | 短影音背景簡報（橫式、亮色／純白、字可改） | `scripts/build_pptx.py` |

## 第 0 步：收資料（一次只問一題，選項要白話）

先讀 Hello Nora 的 `~/.claude/skills/_brand/`（有的話），讀得到的不再問。缺的依序問：
1. 活動名稱、主標、副標
2. 日期、場次時間、地點、費用、每場名額
3. 講師姓名、頭銜、照片
4. 六個主題＋每個一句說明
5. 品牌名稱、LINE ID、加入 LINE 連結
6. 要做哪幾項（預設全部）

## 工作資料夾

在使用者指定處（預設 `~/Downloads/<活動名>/`）建：
```
<活動名>/
├─ poster.html / poster.png / speaker.jpg / NotoSansTC-Bold.ttf / form-qr.svg
├─ 報名頁/  index.html、speaker.jpg、poster.png（給表單用的無 QR 版）、.vercelignore、google-form.gs
└─ 短影音背景/  slides.json、<名稱>.pptx、<名稱>.pdf
```
字體從 `assets/NotoSansTC-Bold.ttf` 複製；`.vercelignore` 從 `templates/vercelignore.txt` 複製。
**改任何既有檔前先備份**：`檔名.bak-YYYYMMDD`（同日 -2、-3）。

## 第 1 步：海報

1. 複製 `templates/poster.html`，照檔頭註解換內容與照片檔名。
2. `scripts/render.sh poster.html poster.png 1080 1920`
3. 自己先看圖：主題列有沒有被資訊欄蓋住、照片邊緣是否生硬、名字有沒有疊到照片上的手。
4. 給使用者看（SendUserFile）。照片有多張就各出一版讓使用者選。

## 第 2 步：Google 表單＋試算表

1. 用內建瀏覽器開 `https://docs.google.com/forms/u/0/`；沒登入 → **請使用者本人登入**（建議用公司帳號），不代填密碼。
2. 開 `https://script.google.com/create`，把 `scripts/google-form.gs` 的 CONFIG 改成本活動內容，用 monaco `setValue` 貼進編輯器 → Cmd+S → 執行 `setupForm`。
3. 跳「需要授權」→ **停下來請使用者自己按**「審查權限 → 選帳號 →（進階 → 前往）→ 允許」。
4. 從執行記錄取得填寫連結、試算表網址與 ID；把 ID 填進 CONFIG.sheetId。
5. 海報圖上線後（第 3 步）再跑 `updateDescription`，表單會變成：短說明 → 海報圖 → 活動介紹 → 題目。
6. 打開表單頁確認內容。

## 第 3 步：報名網頁

1. 複製 `templates/landing.html` 為 `報名頁/index.html`，照檔頭註解換內容。
2. `python3 scripts/form_entries.py <表單 viewform 網址>` → 把 FORM_URL 與 entry ID 換進網頁；**選項文字與表單一字不差**。
3. 另出一張給表單用的海報（隱藏 `.qr,.btn`）存成 `報名頁/poster.png`（`sips -Z 1600` 縮圖）。
4. 用內建瀏覽器手機尺寸（mobile preset）檢查：按鈕、頁尾品牌不斷行、沒有左右捲動。
5. **使用者說要發布才發布**：`cd 報名頁 && vercel deploy --prod --yes`（第一次會建專案）。
6. 發布後：網址加 `?v=` 實測送一筆「測試（可刪）」→ 開試算表確認進來 → 請使用者自己刪那列。

## 第 4 步：QR code

`python3 scripts/make_qr.py <表單或網頁網址> form-qr.svg` → 放到海報右下 → 重出海報。提醒使用者用手機掃一次。

## 第 5 步：短影音背景簡報

1. 先在對話中列出每個主題的「大標題＋副標」給使用者確認；再列「6 個重點」（每條 ≤11 字）確認。
   法規／稅務類重點要附「錄影前請再確認」。
2. 寫 `slides.json`（格式照 `scripts/slides-example.json`；`<em>` 標重點色、`<br>` 換行）。
3. `python3 scripts/build_pptx.py slides.json <名稱>.pptx`（加 `white` 出純白底版）。
4. 驗證：
   ```bash
   osascript -e 'tell application "Keynote"
   set d to open POSIX file "<絕對路徑>.pptx"
   export d to POSIX file "<暫存資料夾>/kn" as slide images with properties {image format:PNG}
   export d to POSIX file "<絕對路徑>.pdf" as PDF
   close d saving no
   end tell'
   ```
   逐頁看圖，確認沒有擠出卡片或斷錯行，再 `open` 給使用者看。
5. 使用者改字 → 改 `slides.json` 重產。重產前先看 .pptx 修改時間，若使用者自己手改過，先問再蓋。

## 改內容時

同一句話常出現在多處（網頁、表單介紹、海報、表單用海報、簡報）。改一處就 grep 其他地方，列給使用者問要不要一起改。
換聯絡方式（LINE、電話、品牌）特別要全掃：海報、網頁頁尾、成功訊息、錯誤提示、表單介紹。

## 交付時一律附上

- 報名網頁網址、表單填寫連結、名單試算表網址（試算表只有擁有者看得到）
- 檔案路徑（用完整絕對路徑）
- 還沒做或沒驗證的事（例如 QR 沒用手機掃過、PPT 沒在 Windows 開過）
- 有 Hello Nora 的話，在 `_brand/marketing-log.md` 的「## 記錄」區加一行（先備份）
