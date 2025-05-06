v# Discord-Cybersecurity-Phishing-Simulation-Toolkit
If the team is using Discord for work, the cybersecurity team can conduct security audits based on the toolkit in this repo.


📓

假設您在Ubuntu 上進行部署，
  1. 所有涉及敏感資訊（e.g Bot Token, Webhook URL, 收集到的憑證）的步驟都必須在 **安全隔離的環境** 下進行，並且嚴格管控存取的權限
  2. 在對團隊成員進行測試前，請先取得正式的授權
  3. 測試結束後，請安全刪除所有收集到的Data, 以免發生糾紛
  4. 測試後務必針對本Repo進行資安教育訓練（以及更多的資安訓練）




---
### 系統架構

- 整體摘要
  - Discord bot 使用檔案`main.py`, 負責透過 Discord 發送釣魚誘餌 (包含連結)。
  - `web_server.py` 負責託管看起來像 Discord 登入頁面的 login.html，並接收用戶在頁面輸入的帳號密碼，再將接收到的敏感資訊發送到一個 Discord Webhook。
  - `login.html` 一個仿造Discord的前端頁面，用來接使用者輸入的值。

- 測試Server
  - 使用Flask Web, 在`web_server.py`設定
  - 透過`login.html`模擬Discord登入介面，讓使用者提供資訊並擔任接值點
  - 接到的值會丟到Discord Webhook

- 其他
  - `.env` 可以將bot TOKEN 和Webhook URL 都一起放進來
  - Webhook URL 和Discord bot TOKEN 請使用者建立並設定
---
### Process

1. 環境建制

```
sudo apt install git
sudo install python3 python3-pip python3-venv
```
> 如果剛建好Ubuntu 則需要`sudo apt update`

2. clone
```
git clone https://github.com/Sakuya4/Discord-Cybersecurity-Phishing-Simulation-Toolkit
cd <存放處>
``` 

3. 開Python的虛擬環境
```
python3 -m venv myenv
source myenv/bin/activate
```

4. 架好Library環境
```
pip install Flask requests discord.py Pillow python-dotenv
```
  - `Flask`: `web_server.py` 創建Web Server 和處理請求
  - `requests`: `web_server.py` 發送Data 到Webhook
  - `discord.py`: `main.py` 的Discord Bot 功能和邏輯實體
  - `Pillow`: `main.py` 處理圖片(discordgift.png)，不過其實可以用別的方式Import
  - `python-dotenv`: 從`.env` 載入環境變數

5. 配置必要TOKEN or Webhook URL到`.env`

6. 啟動服務
   
先啟動Web Server
```
python web_server.py
```
7. 另一台虛擬機啟動Discord bot
   
切記修改好`PHISHING_URL = "https://<釣魚前端網站>/"`
```
python main.py
```

8. 進行LAB

啟動`main.py` 後會有提示告訴你怎麼做。


---
### 部署建議

為了更好的性能、穩定性和安全性，建議將Flask 應用部署在一個標準的WSGI 伺服器上，並使用Apache 或Nginx 作反向代理，

- Apache/Nginx 負責處理 HTTPS 和靜態檔案服務 (如 `login.html`)。
- 它將動態請求 (如 `/login` 的 POST 請求) 轉發給 WSGI 伺服器運行的 Flask 應用。

這種架構比直接使用Flask 內建伺服器更適合測試或準生產環境，但因為測試就直接使用Flask了。


---
### 貢獻

感謝您對本專案感興趣，希望可以一起讓專案變得更好。

///

👾首先，想要宣傳一下我們團隊[輔仁大學資訊系統應用暨人機互動開發團隊](https://github.com/ISHCIL)，是由學生自發組成的團體，如果您對開發網頁應用、人機互動設計或者其他資訊相關領域有興趣歡迎您加入我們。

///

**本專案僅用於資安教育、研究以及在獲得明確授權下的安全測試用途。所有貢獻都應服務於此目的，嚴禁將其用於任何非法或惡意活動。**

如果您有興趣貢獻，以下是一些您可以參與的方向：

* **提升模擬逼真度 (僅限於教育和測試目的)：**
    * 改進前端頁面 (login.html) 的樣式和互動，使其更接近真實的 Discord 登入頁面。
    * 設計更多樣化的釣魚訊息誘餌 (例如不同的禮物類型、通知等)。
* **強化工具自身的安全性與健壯性：**
    * 優化部署架構 (例如集成標準 WSGI 伺服器和反向代理的範例配置)。
    * 改進數據的安全處理方式 (例如更安全的配置加載、加密存儲建議等)。
    * 增加更詳細的日誌記錄和監控功能。
* **擴展防禦教育內容：**
    * 添加如何識別此類釣魚手法的詳細說明和圖示。
    * 增加針對此類攻擊的防禦建議和最佳實踐。
    * 探索並添加其他通訊平台（如 Slack, Teams 等）的釣魚模擬範例 (需確保合法合規)。
* **程式碼優化與維護：**
    * 重構程式碼，提高可讀性和維護性。
    * 修復 Bug 或改進性能。
    * 完善文件說明和設置指南。

**如何貢獻：**

1.  請先 Fork 本倉庫到您的 GitHub 帳戶。
2.  創建一個新的分支來存放您的改動。
3.  提交您的改動，並撰寫清晰的提交訊息。
4.  推送您的分支到您的 Fork 倉庫。
5.  創建一個 Pull Request (PR) 到本倉庫的 `main` 分支。
6.  在 PR 中詳細說明您的改動內容和目的。

在開始較大的改動前，建議先通過 Issue 討論您的想法，以確保方向一致並避免重複工作。

我們期待您的貢獻，一起構建一個有價值的資安教育資源！
