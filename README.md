# Software-Engineering-Cinema-Website

長庚大學資訊工程學系「軟體工程」課程專題。

本專題依課程指定題目，以威秀影城網站為參考進行功能與介面實作，透過團隊合作完成電影資訊、影城資訊、場次查詢、會員功能與訂票流程等網站功能。

本 Repository 為課程團隊專案之個人保存與成果展示版本。原始團隊 Repository 由組員維護且目前為 Private，因此將課程期間參與開發之版本整理於此，並保留相關使用手冊與測試報告。

**Course:** 軟體工程  
**Institution:** 長庚大學 資訊工程學系  
**Project Type:** Team Course Project  
**Backend:** Python  
**Frontend:** HTML / CSS  
**Database:** Python-based Database Module

---

## Repository Structure

```text
Software-Engineering-Cinema-Website/
│
├── app.py
├── database.py
├── requirements.txt
│
├── static/
│   ├── css/
│   └── img/
│
├── templates/
│   └── ...
│
├── reports/
│   ├── User_Manual.pdf
│   └── Test_Report.pdf
│
├── README.md
└── .gitignore
```

---

## Project Overview

本專題以影城網站為題，將網站功能拆分後由團隊共同開發，並透過前後端整合完成可操作的網站系統。

專案內容包含電影與影城資訊呈現、會員相關功能、場次資訊、訂票流程及其他影城網站常見功能。

---

## Main Features

依課程專題實作內容，網站包含：

- 首頁與電影資訊
- 電影列表與電影相關頁面
- 影城資訊
- 場次資訊
- 會員登入與相關功能
- 訂票流程
- 訂單資訊
- 最新消息與活動資訊
- 餐飲相關頁面
- 網站前後端整合

---

## Project Structure

### `app.py`

網站主要應用程式與路由邏輯。

負責接收使用者請求、處理不同頁面的操作流程，並串接資料與前端頁面。

### `database.py`

集中處理專案所需的資料與資料操作功能，使網站邏輯與資料處理能分開管理。

### `static/`

存放網站靜態資源，包括：

- CSS
- Images
- Website assets

不同頁面使用獨立 CSS 檔案，例如電影、訂票、影城、會員與新聞等頁面。

### `templates/`

存放網站各頁面的 HTML Template，並由後端依不同路由載入。

---

## My Contribution

本專案為團隊共同開發，因此 Repository 中包含團隊成員共同完成之程式碼與資源。

我的工作內容以課程期間實際分工為準，主要參與：

- 團隊需求與功能討論
- 網站功能開發與整合
- 程式測試與問題修正
- 專案文件與成果整理

> 詳細個人分工依課程期間之團隊紀錄與報告為準。

---

## Documents

- [`User_Manual.pdf`](./reports/User_Manual.pdf) — 系統操作與使用說明
- [`Test_Report.pdf`](./reports/Test_Report.pdf) — 系統測試內容與結果

---

## What I Learned

這門課與過去以單一程式或演算法為主的課程不同，重點除了功能實作之外，也包含多人協作、需求拆分、系統整合與測試。

在團隊共同開發的過程中，我實際接觸到不同功能模組之間的整合，以及當多人同時修改系統時需要處理的介面、資料與功能一致性問題。

透過使用手冊與測試報告的整理，也讓我理解軟體專案除了「功能可以執行」之外，還需要考慮測試、文件與使用流程，才能形成較完整的軟體系統。

---

## Original Team Repository

原始團隊 Repository 由組員帳號維護，目前為 Private：

`rebeccahou0424/software_engineering_new`

本 Repository 僅作為本人課程學習成果與參與紀錄整理，不代表所有程式碼皆由本人獨立完成。

---

> 本 Repository 為大學課程專題成果整理，網站內容僅供課程學習與非商業展示使用。
