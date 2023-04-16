# ChatGPT with Google

ChatGPTにGoogle検索機能をつけてレスポンスしてくれるWebアプリです。

# Features

現在のChatGPTは学習しているデータが2021年末までのものであり、最新情報に回答してくれません。
そのためLangChainとGoogle APIを使用して、Web検索を元に回答してくれるアプリを作成しました。

# Usage

## Git clone

```
git clone https://github.com/naka-c1024/ChatGPT_with_Google.git
```

## Preparation

### Dockerを使用する場合

```bash
docker build -t gpt_app .
docker run -v $(pwd):/app -p 8080:8080 -it gpt_app bash
```

### Dockerを使用せずローカル環境で実行したい場合

#### Requirement

- Flask 2.1.0
- python-dotenv 1.0.0
- openai 0.27.4
- langchain 0.0.139
- google-api-python-client 2.85.0

#### Installation

```
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

# 使用技術

### 環境: Docker

### フロントエンド: HTML，CSS (TailWindCSS)

### バックエンド: Python (Flask)

### API: Google Programmable Search Engine API, OpenAI API
