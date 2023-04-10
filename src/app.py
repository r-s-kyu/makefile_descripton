import openai
import os
import time
import subprocess
import re

# APIキーの設定
openai.api_key = os.environ['OPENAI_API_KEY']

# プロンプトの設定
PROMPT = "あなたはこれからチャットボットとして振る舞ってください。"

template = """
```
このコマンドを説明して下さい
"""

def main():
    fileobj = open("./Makefile", "r", encoding="utf_8")
    while True:
        line = fileobj.readline()
        match = re.match(r'(\$?)(.*)\:(=?)(.*)', line)
        if line:
            if match:
                if match.groups()[0] == "$":
                    continue
                if match.groups()[2] == "=":
                    continue
                command = match.groups()[1]
                if command == ".PHONY":
                    continue
                
                print("command: " + command)
                input_message = "```\n" + resolve_dependency(command) + template
                output_message = create_response(input_message)
                print(output_message)
                print("\n----------\n")
        else:
            break

    # with open("./Makefile") as f:
    #     makefile = f.read()
    #     input_message = "```\n" + makefile + template

    #     output_message = create_response(input_message)
    #     print(output_message)

def resolve_dependency(make_command):
    cmd = 'make -n ' + make_command
    return (subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')


def create_response(input_message):
    MAX_RETRY = 5
    RETRY_INTERVAL = 1
    for i in range(0, MAX_RETRY):
        try:
            response = openai.Completion.create(model="text-davinci-003", prompt=input_message, temperature=0, max_tokens=1000)
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