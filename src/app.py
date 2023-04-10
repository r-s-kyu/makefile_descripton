import openai
import os
import time

# APIキーの設定
openai.api_key = os.environ['OPENAI_API_KEY']

# プロンプトの設定
PROMPT = "あなたはこれからチャットボットとして振る舞ってください。"

template = """
```
上記のMakefileの内容をコマンドごとに説明してください。 
ただし、形式は下記の形でお願いします。 
```
コマンド
→ 説明
```
また、コマンド引数がある場合はその説明もお願いいたします。

"""

def main():
    with open("./Makefile") as f:
        makefile = f.read()
        input_message = "```\n" + makefile + template

        output_message = create_response(input_message)
        print(output_message)




def create_response(input_message):
    MAX_RETRY = 5
    RETRY_INTERVAL = 1
    for i in range(0, MAX_RETRY):
        try:
            response = openai.Completion.create(model="text-davinci-003", prompt=input_message, temperature=0, max_tokens=3000)
            break
        except:
            if i + 1 == MAX_RETRY:
                print("API接続エラー")
                break
            print("接続をリトライします: {}回目".format(i + 1))
            time.sleep(RETRY_INTERVAL)
            continue

    assistant_response = response.choices[0]["text"]

    return assistant_response

if __name__=="__main__":
    main()