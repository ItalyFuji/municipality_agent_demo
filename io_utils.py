import os
import csv
import pandas as pd

from config import TEXT_OUTPUT_DIR, SUMMARY_CSV_PATH, OUTPUT_DIR


def load_municipality_list(csv_path: str) -> list[dict]:
    df = pd.read_csv(csv_path, encoding="utf-8-sig")

    # 列名の前後の余分な空白の除去
    df.columns = [c.strip() for c in df.columns]

    # 列名のチェック
    if "都道府県" not in df.columns or "市区町村" not in df.columns:
        raise ValueError(
            "入力CSVに「都道府県」もしくは「市区町村」の列が存在しません。"
            f"実際の列名： {list(df.columns)}"
        )
    

    # 結果を貯める空リスト
    records = []
 
       
    # 要素の取り出しとrecordsへの追加
    for _, row in df.iterrows():
        records.append({
            "prefecture": str(row["都道府県"]).strip(),
            "municipality": str(row["市区町村"]).strip()
        })
    return records

# 無ければ出力先フォルダの作成
def ensure_output_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEXT_OUTPUT_DIR, exist_ok=True)

# 都道府県_市区町村.txtの作成
def save_text_file(prefecture: str, municipality: str, summary: str):
    filename = f"{prefecture}_{municipality}.txt"
    filepath = os.path.join(TEXT_OUTPUT_DIR, filename)

    # テキストファイルの中身
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"・{prefecture} {municipality}\n\n")
        f.write(summary.strip() + "\n")

# Summary.csvの作成
def append_to_summary_csv(records: list[dict]):

    # ヘッダーの定義
    field_names = ["都道府県", "市区町村", "概要"]

    # 中身の書き込み
    with open(SUMMARY_CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()

        # 1行ずつ書き込み
        for r in records:
            writer.writerow({
                "都道府県": r["prefecture"],
                "市区町村": r["municipality"],
                "概要": r["summary"],
            })