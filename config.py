import os

# .envファイル用のライブラリ
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

# .envファイルのAPIキーの利用
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# モデルの指定
MODEL_NAME = "gemini-2.5-flash"

# 要約の文字数設定
SUMMARY_LENGTH = 300

# 1件処理するごとに何秒待つか（レート制限対策）
REQUEST_INTERVAL_SEC = 5

# 出力ファイルやパスの指定
OUTPUT_DIR = "output"
TEXT_OUTPUT_DIR = "output/texts"
SUMMARY_CSV_PATH = "output/summary.csv"

# デモ実行用の入力ファイル指定
DEFAULT_INPUT_CSV = "data/input_sample.csv"

