# Preparation 準備工作

This document covers account setup, API key application, certificate activation, and environment configuration for Shioaji.
本文件說明開戶、API 金鑰申請、憑證載入與環境設定。

---

## Overview 概覽

Before using Shioaji, complete these steps:
使用 Shioaji 前，請完成以下步驟：

1. **Open Account 開立帳戶** - Apply for a SinoPac Securities account.
2. **Apply API Key 申請金鑰** - Get your API Key and Secret Key.
3. **Download Certificate 下載憑證** - Get your CA certificate for production trading.
4. **Configure Environment 設定環境** - Set up standard environment variables (`.env`).
5. **Install Environment 安裝環境** - Install Python environment manager `uv` or CLI tool.
6. **Test in Simulation 模擬測試** - Verify login and certificates in simulation mode.

---

## Open Account 開立帳戶

Apply for a SinoPac Securities account:
申請永豐金證券帳戶：

- **Online Application 線上開戶**: [SinoPac Securities Online Opening](https://sinotrade.github.io/zh/tutor/prepare/open_account/)
- Required documents 所需文件: ID card, second ID (drivers license or NHI card), and a bank account for settlement.

---

## Apply API Key 申請金鑰

Shioaji uses API Key for authentication.
Shioaji 使用 API Key 作為登入方式：

1. **Access API Management 進入 API 管理**:
   Go to SinoPac personal service page:
   [SinoPac API Key Management](https://www.sinotrade.com.tw/newweb/PythonAPIKey/)
2. **Create API Key 建立 API Key**:
   - Click "Add API KEY" (新增 API KEY) and complete 2FA verification.
   - Configure key settings: Expiration, Permissions (行情/資料, 帳務, 交易), allowed accounts, and Production/Simulation environment.
   - **IP Whitelist (IP 白名單)**: Restrict allowed IPs (highly recommended).
3. **Save Keys 保存金鑰**:
   - **API Key** - Public identifier.
   - **Secret Key** - Private key (**shown only once! 只顯示一次！**).

---

## Download Certificate 下載憑證

To place orders in production mode, you must activate your CA certificate.
在正式環境中下單，必須載入並啟用憑證。

1. **Download CA Certificate 下載 CA 憑證**:
   - Go to the API management page and click "Download Certificate" (下載憑證).
   - Save the `.pfx` file (e.g., `Sinopac.pfx`).
2. **Store Certificate 存放憑證**:
   - Save the file to a secure directory in your project path.
   - Separate paths on Windows with `/` or double backslashes `\\`.

---

## Environment Variables 環境變數設定

Shioaji 1.5+ standardizes environment variables using the `SJ_` prefix.
Shioaji 1.5+ 採用標準 `SJ_` 前綴環境變數。

Create a `.env` file in your project root:
在專案根目錄（與 `pyproject.toml` 同層）建立 `.env` 檔案：

```ini
# Required API credentials
SJ_API_KEY=YOUR_API_KEY
SJ_SEC_KEY=YOUR_SECRET_KEY

# CA certificate configuration (Required for production ordering)
SJ_CA_PATH=your/ca/path/Sinopac.pfx
SJ_CA_PASSWD=YOUR_CA_PASSWORD

# Environment Mode: true for production, false (or omit) for simulation
SJ_PRODUCTION=false
```

---

## Installation & Setup 安裝與專案建立

### Python Environment (using uv)

[uv](https://docs.astral.sh/uv/) is the recommended Python environment manager.
推薦使用 `uv` 管理 Python 專案與依賴。

```bash
# Install uv
# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Initialize Project
uv init sj-trading --package --app --vcs git
cd sj-trading

# Add Shioaji
uv add shioaji
uv add python-dotenv
```

### Other Languages (via HTTP Server / CLI)

If you are using JavaScript, Go, C++, Rust, etc., you can install the standalone `shioaji` CLI:

```bash
# Install shioaji command
uv tool install shioaji

# Linux / macOS standalone
curl -fsSL https://raw.githubusercontent.com/sinotrade/shioaji/main/install.sh | sh

# Windows standalone (PowerShell)
irm https://raw.githubusercontent.com/sinotrade/shioaji/main/install.ps1 | iex
```

---

## Verification & Testing 驗證與測試

Test your setup in simulation mode to verify credentials.
於模擬環境中驗證登入與憑證是否啟用成功。

### 1. Python SDK Verification

Create a simple script to log in and activate the CA:

```python
import os
import shioaji as sj
from dotenv import load_dotenv

load_dotenv()

def main():
    # Initialize Shioaji in simulation mode
    api = sj.Shioaji(simulation=True)
    
    # Login using environment variables
    api.login(
        api_key=os.environ["SJ_API_KEY"],
        secret_key=os.environ["SJ_SEC_KEY"],
        fetch_contract=False # Set False to speed up testing
    )
    
    # Activate CA Certificate (required for orders)
    api.activate_ca(
        ca_path=os.environ["SJ_CA_PATH"],
        ca_passwd=os.environ["SJ_CA_PASSWD"]
    )
    
    print("Login and CA certificate activation successful!")
    
    # Query CA expiration time
    # Note: Replace with your Person ID (身分證字號) if needed
    person_id = api.stock_account.person_id if api.stock_account else "YOUR_PERSON_ID"
    expire_time = api.get_ca_expiretime(person_id)
    print(f"CA Certificate Expiry: {expire_time}")

if __name__ == "__main__":
    main()
```

Run the script:
```bash
uv run python -m your_package
```

### 2. HTTP Server / CLI Verification

Run the Shioaji local HTTP server, which automatically reads `.env` and activates the CA:

```bash
# Start Shioaji local HTTP server (runs on http://localhost:8080)
shioaji server start

# Check server status
shioaji server check

# Check default accounts list
curl http://localhost:8080/api/v1/auth/accounts

# Check CA certificate expiration date
curl "http://localhost:8080/api/v1/auth/ca_expiretime?person_id=YOUR_PERSON_ID"
```

To stop the server:
```bash
shioaji server stop
```

---

## Checklist 檢查清單

Before going live (production mode) 上線正式環境確認：

- [ ] Account opened 帳戶已開立
- [ ] API Key created and permissions checked 已建立 API Key 並勾選權限
- [ ] CA Certificate downloaded and path set 已下載憑證且路徑設定正確
- [ ] Standard env variables configured (`SJ_API_KEY`, `SJ_SEC_KEY`, etc.)
- [ ] API Terms of Service signed on website 已在官網簽署條款
- [ ] Simulation mode login test passed 模擬環境登入測試通過

---

## Reference 參考資料

- Account Opening 開戶: [SinoPac Securities Online Opening](https://sinotrade.github.io/zh/tutor/prepare/open_account/)
- API Key Application 金鑰申請: [SinoPac API Key Guide](https://sinotrade.github.io/zh/tutor/prepare/token/)
- Terms of Service 條款簽署: [SinoPac Terms Guide](https://sinotrade.github.io/zh/tutor/prepare/terms/)
