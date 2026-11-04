// event-kit：一鍵建 Google 報名表單＋回覆試算表，並可重複更新介紹文字與海報圖
// 用法：script.google.com 新專案 → 整段貼上 → 改 CONFIG → 執行 setupForm（只跑一次）
//       之後改介紹或換海報：把 setupForm 執行記錄印出的試算表 ID 填進 CONFIG.sheetId → 執行 updateDescription
// 第一次執行會跳 Google 授權視窗，必須由使用者本人按「允許」。
// 範例內容＝小室房屋 11/17 房東分享會。

var CONFIG = {
  title: '房東出租全攻略｜11/17 屋主分享會報名',
  shortDesc: '當個完全躺平的房東｜主講：小室房屋創辦人 李秉誠\n📅 11/17（二）14:00／19:00 兩場次・每場限 20 位',
  confirmation: '報名成功！我們會在活動前透過 LINE 或電話跟您確認場次，11/17 見 🙌',
  sessions: ['下午場 14:00–16:30', '晚上場 19:00–21:30'],
  statuses: ['已經在出租，自己管', '已委託代管／包租', '房子空著，準備出租', '還沒有房子，先來了解'],
  askTitle: '最想問講師的問題（選填）',
  sheetName: '11/17 房東分享會報名名單',
  // 表單最上方的海報圖（要是公開網址；通常放在報名網頁同一個 Vercel 專案裡）
  posterUrl: 'https://littlethings-landlord-talk.vercel.app/poster.png',
  // setupForm 跑完後填入（執行記錄會印出）
  sheetId: '',
  detail: [
    '當房東，你是不是也遇過這些事？',
    '・房客看起來不錯，住進來才發現問題一堆',
    '・租約是網路抄的，出事才發現該寫的沒寫到',
    '',
    '━━━━━━━━━━━━',
    '2.5 小時，房東出租六大關鍵',
    '01 租客篩選｜挑到準時繳租、優質的好租客',
    '02 租約｜哪些條款一定要寫進去，保護你也保護房子',
    '',
    '━━━━━━━━━━━━',
    '活動資訊',
    '📅 11/17（二）下午場 14:00–16:30／晚上場 19:00–21:30',
    '📍 台北市大同區民生西路105號2樓（Nextdoor Space 隔壁空間）',
    '💰 場地費 NT$200（現場繳交）',
    '👥 每場限 20 位，額滿即止',
    '',
    '有問題歡迎洽 LINE ID：@847qcmyz'
  ]
};

function setupForm() {
  var form = FormApp.create(CONFIG.title);
  form.setDescription(CONFIG.shortDesc)
    .setConfirmationMessage(CONFIG.confirmation)
    .setCollectEmail(false)
    .setAllowResponseEdits(false)
    .setLimitOneResponsePerUser(false);

  form.addTextItem().setTitle('姓名').setRequired(true);

  var phoneRule = FormApp.createTextValidation()
    .setHelpText('請填 09 開頭的 10 碼手機號碼')
    .requireTextMatchesPattern('^09[0-9]{8}$')
    .build();
  form.addTextItem().setTitle('手機').setHelpText('例：0912345678')
    .setValidation(phoneRule).setRequired(true);

  var ses = form.addMultipleChoiceItem().setTitle('想參加的場次').setRequired(true);
  ses.setChoices(CONFIG.sessions.map(function (s) { return ses.createChoice(s); }));

  var st = form.addMultipleChoiceItem().setTitle('目前狀況');
  st.setChoices(CONFIG.statuses.map(function (s) { return st.createChoice(s); }));

  form.addParagraphTextItem().setTitle(CONFIG.askTitle);

  var ss = SpreadsheetApp.create(CONFIG.sheetName);
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log('填寫連結：' + form.getPublishedUrl());
  Logger.log('名單試算表：' + ss.getUrl());
  Logger.log('試算表 ID（填進 CONFIG.sheetId）：' + ss.getId());
}

// 更新介紹文字＋海報圖：可重複執行。順序固定＝短說明 → 海報圖 → 活動介紹 → 題目
// （Google 表單的圖片放不到標題上方）
function updateDescription() {
  var ss = SpreadsheetApp.openById(CONFIG.sheetId);
  var form = FormApp.openByUrl(ss.getFormUrl());
  form.setDescription(CONFIG.shortDesc);

  form.getItems(FormApp.ItemType.IMAGE).forEach(function (it) { form.deleteItem(it); });
  if (CONFIG.posterUrl) {
    var img = UrlFetchApp.fetch(CONFIG.posterUrl).getBlob();
    var item = form.addImageItem().setImage(img).setTitle('').setWidth(740);
    form.moveItem(item.getIndex(), 0);
  }

  form.getItems(FormApp.ItemType.SECTION_HEADER).forEach(function (it) { form.deleteItem(it); });
  var sec = form.addSectionHeaderItem().setTitle('活動介紹').setHelpText(CONFIG.detail.join('\n'));
  form.moveItem(sec.getIndex(), CONFIG.posterUrl ? 1 : 0);

  Logger.log('已更新：' + form.getPublishedUrl());
}
