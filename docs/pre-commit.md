# pre-commit 操作指南

> 如果你沒有安裝 uv，請去參考官方文件安裝，我們將使用 uv 用作本專案的 python 套件管理。
> <https://docs.astral.sh/uv/getting-started/installation/>

本專案使用 pre-commit 來規範程式碼風格以及相關測試與檢查，降低爛程式碼出現在 commit 裡面的機率。務必在開發前先安裝好 pre-commit 到 repo 裡面：

```bash
uvx pre-commit install
```

安裝完後，可以先跑一次全域的 pre-commit，確認功能正常。

```bash
uvx pre-commit run --all-file
```

後續開發過程中如果要跑檢查，就執行：

```bash
uvx pre-commit run
```

在 commit 前也會跑一次確保你的 commit 是~~乾淨的程式碼~~，至少不會有基本的錯誤。
