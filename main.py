import os

from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
import openai
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent

load_dotenv()
# Make sure API key is set
if not os.environ["OPENAI_API_KEY"] or not os.environ["GOOGLE_API_KEY"] or not os.environ["GOOGLE_CSE_ID"]:
    raise RuntimeError("API key not set")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # POST メソッドでアクセスされた場合
    if request.method == "POST":

        # openaiをそのままつかう場合
        '''
        user_msg = request.form["user_msg"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                # {"role": "system", "content": "ここで役割を指定する。"},
                # {"role": "user", "content": '初メッセージ'},
                # {"role": "assistant", "content": 'レスポンスを入れる'},
                {"role": "user", "content": user_msg},
            ],
        )
        res_msg = response.choices[0]["message"]["content"]
        '''

        # langchainをつかう場合
        '''
        #プロンプト
        prompt = request.form["user_msg"]
        #LLMの設定
        llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.environ["OPENAI_API_KEY"])
        #推論を実行
        res_msg = llm(prompt)
        '''

        # Google検索をつかう場合(https://murasan-net.com/index.php/2023/04/03/chatgpt-langchain-web-newinfo/)
        # LLMを設定
        llm = OpenAI(model_name="gpt-3.5-turbo")
        # ツールを設定
        tools = load_tools(["google-search"], llm=llm)
        # エージェントの作成
        agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=False)
        # 推論を実行
        res_msg = agent.run(request.form["user_msg"])

        return render_template("index.html", res_msg=res_msg)

    # GET メソッドでアクセスされた場合
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
