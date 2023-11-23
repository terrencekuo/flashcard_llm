from llama_cpp.llama import Llama, LlamaGrammar
import json
import logging  
import os

MODEL_NAME = os.environ['MODEL_NAME']
llm = Llama(model_path=f"./model/{MODEL_NAME}")
logger = logging.getLogger()

grammar_text = r'''
root   ::= object
value  ::= object | array | string | number | ("true" | "false" | "null") ws

object ::=
  "{" ws (
            string ":" ws value
    ("," ws string ":" ws value)*
  )? "}" ws

array  ::=
  "[" ws (
            value
    ("," ws value)*
  )? "]" ws

string ::=
  "\"" (
    [^"\\] |
    "\\" (["\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F]) # escapes
  )* "\"" ws

number ::= ("-"? ([0-9] | [1-9] [0-9]*)) ("." [0-9]+)? ([eE] [-+]? [0-9]+)? ws

# Optional space: by convention, applied in this grammar after literal chars when allowed
ws ::= ([ \t\n] ws)?
'''
grammar = LlamaGrammar.from_string(grammar_text)

def validate_input(input_string):
    print("input_str: " + input_string)
    try:
        # Attempt to parse the input string as a JSON list
        words = json.loads(input_string)
        return True
    except json.JSONDecodeError as e:
        logger.info("invalid_json=\"{}\"".format(e))
        # Input is not a valid JSON list
        return False

def handler(event, context):
    prompt = event['prompt']
    logger.info("prompt=\"{}\"".format(prompt))

    if not validate_input(prompt):
        return "{\"error\": \"invalid input\"}"

    llm_input = "You are an english teacher. I will give you words to add to your word bank which you will use to create phrases and sentences to help me learn the language. Your word bank only contains: `{}`. Create 2 sentences and phrases only using the words in your word bank. You must output a JSON with key as `output` and the value as an array containing the generated sentences and phrases".format(prompt)

    max_tokens = int(event['max_tokens'])    

    output = llm(llm_input, max_tokens=max_tokens, echo=True)
    response = llm(
        llm_input,
        grammar=grammar, max_tokens=-1
    )

    logger.info("response=\"{}\"".format(response))
    text_result = response["choices"][0]["text"]
    data = json.loads(text_result)
    data_dump = json.dumps(data, indent=4)
    logger.info("output=\"{}\"".format(data_dump))

    return {
        'statusCode': 200,
        'body': data_dump,
        'headers': {
            'Content-Type': 'application/json'
        }
    }
