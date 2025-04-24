# 檔案瀏覽器應用

這是一個基於 Flask 的檔案瀏覽器應用，專門用於瀏覽和查看 Markdown 文件及其相關的參考資料和思路文件。

## 功能特點

- 瀏覽專案目錄結構
- 查看 Markdown 文件並轉換為 HTML 顯示
- 支援顯示與文件相關的參考資料（`.reference` 文件）
- 支援顯示與文件相關的思路文件（`.think` 文件）
- 支援顯示網站架構思路（`.website-outline.think` 文件）
- 支援顯示目錄簡介（`.profile` 文件）

## 檔案結構說明

```
file_browser/           # 應用主目錄
├── __init__.py         # Python 包初始化文件
├── app.py              # 主應用程式
├── static/             # 靜態資源目錄
│   └── css/            # CSS 樣式文件
│       └── style.css   # 主要樣式文件
└── templates/          # HTML 模板目錄
    ├── browse.html     # 瀏覽目錄的模板
    ├── index.html      # 首頁模板
    ├── layout.html     # 基礎布局模板
    └── view.html       # 查看文件的模板

data/                   # 資料目錄
└── [專案名稱]/          # 各個專案目錄
    ├── .profile        # 專案簡介文件
    ├── documents.jsonl # 文件索引
    ├── documents.xml   # 文件結構
    └── website/        # 網站內容目錄
        └── zh-TW/      # 中文內容
            ├── .website-outline      # 網站結構文件
            ├── .website-outline.think # 網站架構思路文件
            └── [分類目錄]/            # 各分類目錄
                ├── [文件名].md        # Markdown 文件
                ├── .[文件名].reference # 參考資料文件
                └── .[文件名].think    # 思路文件
```

## 特殊文件說明

- `.profile`: 目錄簡介文件，顯示在目錄列表中
- `.website-outline`: 網站結構文件，定義網站的頁面結構
- `.website-outline.think`: 網站架構思路文件，說明網站整體架構的設計思路
- `.[文件名].reference`: 參考資料文件，包含與特定文件相關的參考資料
- `.[文件名].think`: 思路文件，包含與特定文件相關的設計思路

## 安裝與運行

### 安裝依賴

使用 uv 安裝依賴：

```bash
uv add flask markdown
```

或使用 pip 安裝依賴：

```bash
pip install flask markdown
```

### 運行應用

```bash
python run.py
```

應用將在 http://localhost:8080 啟動。

## 使用方法

1. 啟動應用後，訪問 http://localhost:8080
2. 首頁將顯示所有可用的專案目錄
3. 點擊專案目錄進入瀏覽模式
4. 在瀏覽模式中，可以查看目錄結構、網站架構和網站架構思路
5. 點擊文件可以查看文件內容、參考資料和思路

## 開發說明

- 應用基於 Flask 框架開發
- 使用 Markdown 庫將 Markdown 內容轉換為 HTML
- 使用 Bootstrap 進行前端樣式設計
- 支援多標籤頁顯示不同類型的內容
