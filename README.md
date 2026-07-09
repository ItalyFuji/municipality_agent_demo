# municipality_agent_demo
municipality_agent/  
├── main.py              ← これを実行する(エントリーポイント)  
├── agent.py             ← エージェント本体(Gemini + Wikipediaツール)  
├── config.py            ← モデル名、待機秒数などの設定  
├── io_utils.py          ← CSV読み込み・書き出し、テキスト出力  
├── requirements.txt  
├── .env.example         ← .env にコピーしてAPIキーを設定  
├── data/input_sample.csv ← 動作確認用サンプル(3件)  
└── output/               ← 実行すると自動生成される  
     ├── summary.csv  
     └── texts/{都道府県_市区町村}.txt  
