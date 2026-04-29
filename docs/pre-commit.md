# pre-commit 操作指南

> 如果你沒有安裝 uv，請去參考官方文件安裝，我們將使用 uv 用作本專案的 python 套件管理。
> <https://docs.astral.sh/uv/getting-started/installation/>

本專案使用 pre-commit 來規範程式碼風格以及相關測試與檢查，降低爛程式碼出現在 commit 裡面的機率。務必在開發前先安裝好 pre-commit 到 repo 裡面：

```bash
uvx pre-commit install --install-hooks
```

這會同時安裝 `pre-commit` 與 `commit-msg` hooks，所以除了既有的程式碼檢查外，commit message 也會在 `git commit` 時一起驗證。

安裝完後，可以先跑一次全域的 pre-commit，確認功能正常。

```bash
uvx pre-commit run --all-files
```

後續開發過程中如果要跑檢查，就執行：

```bash
uvx pre-commit run
```

在 commit 前也會跑一次確保你的 commit 是~~乾淨的程式碼~~，至少不會有基本的錯誤。

## 驗證 commit message hooks

你可以用下面指令手動驗證 commit message 規則：

```bash
printf 'feat(frontend): add login form\n' > /tmp/commit-msg-valid.txt
uvx pre-commit run --hook-stage commit-msg commit-message-check --commit-msg-filename /tmp/commit-msg-valid.txt
```

如果你想確認失敗訊息，也可以測試一個不合法的例子：

```bash
printf 'fix: misc changes\n' > /tmp/commit-msg-invalid.txt
uvx pre-commit run --hook-stage commit-msg commit-message-check --commit-msg-filename /tmp/commit-msg-invalid.txt
```
