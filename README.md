# SesameBot

Sesame スマートロックを操作する

## Render

ダッシュボードの Build / Start は次にする。既存サービスは作成時の Python（例: 3.11.9）が `PYTHON_VERSION` に残っていることがある。環境変数は次にする。

- `PYTHON_VERSION` = `3.14.3`（完全修飾必須。`.python-version` より優先される）

**Build Command**

```text
uv sync --frozen --no-dev
```

**Start Command**

```text
uv run sesame-bot
```
