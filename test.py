from llama_cpp.llama import Llama, LlamaGrammar
import json
import sys

val = input("enter word bank:\n")

def validate_input(input_string):
    print("input_str: " + input_string)
    try:
        # Attempt to parse the input string as a JSON list
        words = json.loads(input_string)
        return True
    except json.JSONDecodeError as e:
        print("Invalid JSON syntax:", e)
        # Input is not a valid JSON list
        return False

if validate_input(val):
    print("Valid list of words!")
else:
    print("Invalid input.")
    sys.exit(1)

llm_input = "You are an english teacher. I will give you words to your word bank which you will use to create phrases and sentences to help me learn the language. Your word bank contains: `{}`. Please output a JSON with the `output` as your key containing 4 sentences and phrases which only use the words in your word bank.".format(val)
print("input: " + llm_input)

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
llm = Llama("llama-2-7b-chat.Q4_K_M.gguf")

response = llm(
    llm_input,
    grammar=grammar, max_tokens=-1
)
text_result = response["choices"][0]["text"]
data = json.loads(text_result)
print(json.dumps(data, indent=4))
