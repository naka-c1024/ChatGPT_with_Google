import os

from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
import openai

load_dotenv()
# Make sure API key is set
if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not set")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # POST メソッドでアクセスされた場合
    if request.method == "POST":
        # AIに送るメッセージ
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
        return render_template("index.html", res_msg=res_msg)

    # GET メソッドでアクセスされた場合
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
