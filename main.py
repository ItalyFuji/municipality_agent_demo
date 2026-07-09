import sys
import time

from config import DEFAULT_INPUT_CSV, REQUEST_INTERVAL_SEC
# 各ファイルから必要な関数・定数をインポート
from io_utils import (
    load_municipality_list,
    ensure_output_dirs,
    save_text_file,
    append_to_summary_csv,
)
from agent import build_agent, summarize_municipality

# main関数
def main():
    # 入力フォルダの指定
    input_csv = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT_CSV

    print(f"[INFO] 入力CSV: {input_csv}")
    # 市区町村リストの取得
    records = load_municipality_list(input_csv)
    print(f"[INFO] {len(records)}件の市区町村を処理中。")

    # 出力フォルダの準備
    ensure_output_dirs()
    # エージェントの組み上げ
    executor = build_agent()

    # 結果用空リスト
    results = []

    # 進捗表示、iは今何件目か
    for i, rec in enumerate(records, start=1):
        pref, muni = rec["prefecture"], rec["municipality"]
        print(f"[{i}/{len(records)} {pref}{muni}を処理中...]")

        try:
            summary = summarize_municipality(executor, pref, muni)
        except Exception as e:
            # レート制限(429)に達したら残りをスキップして出力へ
            if "Quota exceeded" in str(e) or "ResourceExhausted" in str(e):
                print(f"[WARN] APIの上限に達しました。残り{len(records) - i}件をスキップします。")
                break
            print(f"[WARN] 失敗しました: {e}")
            # エラー用要約文
            summary = "(取得に失敗しました。時間をおいて再実行してください。)"

        save_text_file(pref, muni, summary)
        results.append({"prefecture": pref, "municipality": muni, "summary": summary})

        # まだ次がある時だけ待機
        if i < len(records):
            time.sleep(REQUEST_INTERVAL_SEC)

    append_to_summary_csv(results)
    print(f"[INFO] {len(results)}件を出力しました。output/フォルダを確認してください。")
    print(f" - 一覧CSV: output/summary.csv")
    print(f" - 個別テキスト: output/texts/ 以下")

# 「python main.py」と実行された時だけmain()を呼び出し
if __name__ == "__main__":
    main()