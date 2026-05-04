# Commit Message 規範

本專案的 commit message 參考 [Conventional Commits](https://www.conventionalcommits.org/)，並加入較嚴格的 title、scope、body 規則，讓人類 reviewer 與 agent 都能從 history 理解「為什麼」以及「怎麼改」。

## Header 格式

```text
type(scope): subject
type: subject
```

目前 commit-msg hook 允許的 `type`：

- `feat`: 新功能
- `fix`: 修 bug
- `docs`: 文件
- `test`: 測試
- `refactor`: 不改變外部行為的重構
- `chore`: 維護性工作
- `ci`: CI 設定
- `build`: build 或相依性設定
- `perf`: 效能改善
- `style`: 純格式或風格調整

`subject` 必須描述一件具體事情，使用小寫祈使動詞開頭，不要句號結尾。

```text
feat(auth): add login token refresh
fix(frontend): handle empty profile response
docs: add commit message guidelines
```

避免把多件事情塞進同一個 title：

```text
fix: update auth and frontend and tests
```

## Scope 規則

`scope` 用來標示變更主要影響的 domain 或 codebase section。選擇標準是：**讀者看到 scope 後，應該能快速知道要去哪個區域 review。**

建議優先使用這些 scope：

- `auth`: 註冊、登入、JWT、密碼雜湊、驗證 dependency。
- `users`: 使用者模型、profile、admin user 管理。
- `core`: 設定、資料庫 session、共用 exception、安全性基礎設施。
- `face`: 臉部註冊、辨識、訓練、embedding 相關流程。
- `frontend`: Vue UI、routing、Pinia store、前端測試。
- `firmware`: Pico W 韌體、CMake、Pico SDK 設定。
- `docs`: 文件、貢獻指南、commit/pre-commit 規範。
- `tooling`: 本地開發工具、scripts、lint、format、pre-commit hooks。
- `ci`: GitHub Actions 或其他 CI/CD 設定。
- `config`: 專案設定、環境設定、build config。
- `deps`: dependency 或 lockfile 更新。
- `tests`: 測試基礎設施、fixtures、coverage 設定。

pre-commit 只檢查 commit header 格式、type 與 subject 品質，不強制限制 scope 清單。新增 scope 前，請先確認它代表穩定 domain 或 codebase section；不要為一次性檔案或臨時改動發明 scope。

不要使用 `router`、`service`、`schemas`、`models` 這類 layer 名稱作為 scope；`type` 已經表示改動種類，也不要用 scope 表達 `fix`、`test`、`refactor` 這類 class。

當一個 commit 橫跨多個 scope，先檢查是否應該拆成多個 commit。只有在同一件邏輯變更必須同時碰多個區域時，才省略 scope 或使用最主要的 scope。

## Body 寫法

只要變更不是非常小，請寫 body。Body 的重點不是列檔案，而是說清楚推理過程，接近 Linux kernel commit message 的風格：

1. 原本遇到什麼問題或限制。
2. 為什麼目前的做法不夠好。
3. 這個 commit 做了什麼改動。
4. 改完後的行為、風險或驗證方式。

範例：

```text
fix(auth): reject expired access tokens

Expired JWTs were decoded without checking the exp claim, so protected
routes could accept stale credentials.

Validate token expiration in the auth dependency before loading the user.
This keeps route handlers unchanged while centralizing the rejection path.

Verified with backend auth dependency tests.
```

## Pre-commit 與驗證

開發前請先安裝 hooks，詳見 [pre-commit 操作指南](./pre-commit.md)。

```bash
uvx pre-commit install --install-hooks
uvx pre-commit run --all-files
```

依變更範圍執行測試（完整指令列表見 [AGENTS.md](../AGENTS.md#build-test-and-development-commands)）：

- Backend coverage: `cd backend && uv run pytest tests --cov`

影響 `auth`、`users`、`core`、`face` 或共用流程的 backend 變更，PR 前應補測試並檢查 coverage。若無法執行某項驗證，請在 PR 說明中寫明原因。
