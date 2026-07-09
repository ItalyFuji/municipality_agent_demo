# LangchainからGeminiモデルを呼び出すためのクラス
from langchain_google_genai import ChatGoogleGenerativeAI

# Wikipediaへのアクセス用
from langchain_community.tools import WikipediaQueryRun

# LangChainのツールとして使えるようにラップしたもの
from langchain_community.utilities import WikipediaAPIWrapper

# 「考える→ツールを使う→また考える」というReAct方式のエージェントを組み立てる関数とエージェントの実行役
from langchain.agents import create_react_agent, AgentExecutor

from langchain.prompts import PromptTemplate

# configより設定値の読み込み
from config import GOOGLE_API_KEY, MODEL_NAME, SUMMARY_LENGTH


# エージェントを組み立てる関数
def build_agent() -> AgentExecutor:
    
    # Geminiモデルのインスタンス作成
    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        # 出力のランダム性の度合い
        # 0に近いほど毎回似た堅実な出力、高いほど多様でブレやすい出力
        temperature=0.3,
    )

    # Wikiの検索設定
    wiki_wrapper = WikipediaAPIWrapper(
        # 日本語版Wikiを対象
        lang="ja",
        # 検索結果上位1件のみを使用
        top_k_results=1,
        # 取得する本文の文字数制限
        doc_content_chars_max=3000,
    )

    # エージェントに渡すための設定のツール化
    wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)
    # ツールのリスト化
    tools = [wiki_tool]

    # ReAct方式の標準プロンプトをローカルで定義
    prompt = PromptTemplate.from_template(
        "Answer the following questions as best you can. You have access to the following tools:\n\n"
        "{tools}\n\n"
        "Use the following format:\n\n"
        "Question: the input question you must answer\n"
        "Thought: you should always think about what to do\n"
        "Action: the action to take, should be one of [{tool_names}]\n"
        "Action Input: the input to the action\n"
        "Observation: the result of the action\n"
        "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
        "Thought: I now know the final answer\n"
        "Final Answer: the final answer to the original input question\n\n"
        "Begin!\n\n"
        "Question: {input}\n"
        "Thought:{agent_scratchpad}"
    )

    # LLM・ツール・プロンプトの3つを組み合わせエージェントの頭脳部分を作成
    agent = create_react_agent(llm, tools, prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        # 途中経過をターミナルに表示
        verbose=True,
        # LLMの出力形式が崩れエラーになった際に止まらず自動でリトライを試みる
        handle_parsing_errors=True,
        # 考える→行動するのループが5回を超えたら強制打ち切り
        max_iterations=5,
    )
    return executor

# 1つの市区町村に対する処理
def summarize_municipality(executor: AgentExecutor, prefecture:str, municipality:str) -> str:

    # エージェントに投げる指示（プロンプト）
    query = (
        f"{prefecture}{municipality}についてWikipediaツールを使って調べてください。"
        f"人口、地理的特徴、歴史、産業などの観点を踏まえて観光情報について、"
        f"日本語で{SUMMARY_LENGTH}字程度の紹介文を1つだけ作成してください。"
        f"検索過程の説明や前置きは不要です。紹介分の本文のみを出力してください。"
        f"検索は一度だけ実行してください。"
    )

    # エージェントの実行
    result = executor.invoke({"input": query})
    return result["output"]
