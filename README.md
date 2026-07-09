# municipality_agent_demo

練習もかねて製作したWikipediaを使って市区町村の紹介文を自動生成するLangChainエージェントのデモ。  
GeminiモデルとWikipediaツールを組み合わせたReActエージェントが、指定した市区町村ごとに紹介文を生成しCSVとテキストファイルに出力する。

---

## ディレクトリ構造

```
municipality_agent/
├── main.py               ← これを実行する（エントリーポイント）
├── agent.py              ← エージェント本体（Gemini + Wikipediaツール）
├── config.py             ← モデル名、待機秒数などの設定
├── io_utils.py           ← CSV読み込み・書き出し、テキスト出力
├── requirements.txt
├── .env.example          ← .envにコピーしてAPIキーを設定
├── data/input_sample.csv ← 動作確認用サンプル
└── output/               ← 実行すると自動生成される
    ├── summary.csv
    └── texts/{都道府県}_{市区町村}.txt
```

---

## セットアップ

### 1. 仮想環境の作成と有効化

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

終了するときは：

```bash
deactivate
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. APIキーの設定

`.env.example`をコピーして`.env`を作成し、Google AI Studioで取得したAPIキーを記入する。

```bash
cp .env.example .env
```

```
# .env
GOOGLE_API_KEY=your_api_key_here
```

APIキーは[Google AI Studio](https://aistudio.google.com/)で無料取得できる。

---

## 実行方法

### サンプルデータで実行

```bash
python main.py
```

`data/input_sample.csv`を入力として処理し、結果を`output/`に出力する。

### 任意のCSVを指定して実行

```bash
python main.py path/to/your_input.csv
```

入力CSVは以下の形式（ヘッダー必須）：

```csv
都道府県,市区町村
東京都,港区
大阪府,大阪市
```

---

## 出力

| ファイル | 内容 |
|----------|------|
| `output/summary.csv` | 全件の紹介文をまとめたCSV |
| `output/texts/{都道府県}_{市区町村}.txt` | 市区町村ごとの紹介文テキスト |

---

## 現在の課題

### APIの無料枠が非常に少ない

Google AI Studioの無料枠は**モデルごとに20リクエスト/日**に制限されている。  
1件の処理でLLMを2〜3回呼び出すため、実質**6〜7件/日**しか処理できない。

市区町村は全国で1700件以上あるため、無料枠のみでの全件処理は現実的でない。

**対応策の候補：**
- Google AIの従量課金を有効にする（1件あたり数円程度）
- Groqなど無料枠の大きい別プロバイダーに切り替える

### レート制限時の挙動

上限に達した場合は、その時点で処理を打ち切りそれまでの結果を出力する。  
翌日（クォータリセット後）に残りの件数から再実行することを推奨する。  
※再実行時は既存の`output/summary.csv`に追記される。
