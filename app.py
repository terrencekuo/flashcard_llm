from llama_cpp.llama import Llama, LlamaGrammar
import json
import os
#import subprocess
from huggingface_hub import hf_hub_download

# set up llama grammar
grammar_text = r'''
root ::= "[" items "]" EOF

items ::= item ("," ws* item)*

item ::= string

string  ::=
  "\"" word (ws+ word)* "\"" ws*

  word ::= [a-zA-Z]+

  ws ::= " "

  EOF ::= "\n"
'''
grammar = LlamaGrammar.from_string(grammar_text)

# set up the llama.cpp
MODEL_NAME = os.environ['MODEL_NAME']
llm = ""

def validate_input(input_string):
    print("input_str={}".format(input_string))
    try:
        # Attempt to parse the input string as a JSON list
        words = json.loads(input_string)
        return True
    except json.JSONDecodeError as e:
        print("invalid_json={}".format(e))
        # Input is not a valid JSON list
        return False

def handler(event, context):
    global llm

    # download and init model
    # NOTE: we do this here because the lambda init runtime is only 10s
    if llm == "":
        print("installing model and init llama.cpp")

        # install the model
        # HF_HOME is used to config the hugging face cache dir
        # HF_HUB_ENABLE_HF_TRANSFER is used to config high speed download
        #result = subprocess.run('HF_HOME="/tmp" HF_HUB_ENABLE_HF_TRANSFER=1 huggingface-cli download terrencekuo/zephyr-7b-backup zephyr-7b-beta.Q4_K_M.gguf --local-dir /tmp --local-dir-use-symlinks False', shell=True)
        hf_hub_download(repo_id="terrencekuo/zephyr-7b-backup", filename="zephyr-7b-beta.Q4_K_M.gguf", cache_dir="/tmp/cache", local_dir="/tmp/model", local_dir_use_symlinks=False)
        llm = Llama(model_path=f"/tmp/model/{MODEL_NAME}")

    print("start lambda handler event={}".format(event))

    # Default values
    default_word_bank = '["hello", "good morning", "I", "like", "eat", "drink", "rice", "water"]'
    default_num_results = 5
    default_max_tokens = 1024

	# populate param
    word_bank = event.get('word_bank', default_word_bank)
    try:
        num_results = int(event.get('num_results', default_num_results))
    except ValueError:
        num_results = default_num_results
    try:
        max_tokens = int(event.get('max_tokens', default_max_tokens))
    except ValueError:
        max_tokens = default_max_tokens

    if not validate_input(word_bank):
        return {
            'statusCode': 400,
            'body': "{\"error\": \"invalid word_bank\"}",
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    llm_input = "You are an english teacher. I will give you words to add to your word bank which you will use to create phrases and sentences to help me learn the language. Your word bank only contains: `{word_bank}`. Create {num_results} sentences and phrases only using the words in your word bank. You must output an array containing the generated sentences and phrases".format(word_bank = word_bank, num_results = num_results)
    print("llm_input=\'{}\'".format(llm_input))

    output = llm(llm_input, max_tokens=max_tokens, echo=True)
    response = llm(
        llm_input,
        grammar=grammar,
        max_tokens=-1
    )

    print("full_llm_response={}".format(response))
    text_result = response["choices"][0]["text"]
    data = json.loads(text_result)
    data_dump = json.dumps(data, separators=(',', ':'))
    print("llm_output={}".format(data_dump))

    return {
        'statusCode': 200,
        'body': data_dump,
        'headers': {
            'Content-Type': 'application/json'
        }
    }
