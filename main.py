import os

from flask import Flask, request, render_template
from dotenv import load_dotenv
from langchain.agents import ZeroShotAgent, AgentExecutor, load_tools
from langchain import OpenAI, LLMChain

# 環境変数を読み込む
load_dotenv()

# APIキーが設定されていることを確認
if not os.environ["OPENAI_API_KEY"] or not os.environ["GOOGLE_API_KEY"] or not os.environ["GOOGLE_CSE_ID"]:
    raise RuntimeError("APIキーが設定されていません")

app = Flask(__name__)

def create_agent_executor():
    """
    エージェント実行者のインスタンスを作成して、ユーザー入力を処理します。
    """
    llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo")
    tools = load_tools(["google-search"], llm=llm)
    prompt = create_agent_prompt(tools)

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

    return agent_executor

def create_agent_prompt(tools):
    """
    ZeroShotAgent用のエージェントプロンプトを作成します。
    """
    prefix = """次の質問にできる限り答えてください。次のツールにアクセスできます:"""
    suffix = """最終的な答えを出すときは、日本語で出力してください。

    Question: {input}
    {agent_scratchpad}
    """

    return ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input", "agent_scratchpad"]
    )

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # ユーザー入力を処理するエージェント実行者を作成
        agent_executor = create_agent_executor()

        # エージェントの実行中に発生する例外を処理
        try:
            res_msg = agent_executor.run(request.form["user_msg"])
        except ValueError as e:
            res_msg = f"エラーが発生しました: {str(e)}"
        except Exception as e:
            res_msg = f"予期しないエラーが発生しました: {str(e)}"

        return render_template("index.html", res_msg=res_msg)

    # GETリクエストの場合、メインページを表示
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

'''
参考
https://murasan-net.com/index.php/2023/04/03/chatgpt-langchain-web-newinfo/
https://note.com/npaka/n/nd9a4a26a8932
'''
