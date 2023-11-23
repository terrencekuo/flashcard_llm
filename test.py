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
llm_input = "You are an english teacher. I will give a word bank which you will use to create sentences to help me practice the language. Your provided word bank is the following list of strings:`{}`. Output 5 sentences, only using the words in your word bank, as a list. Sentences must be direct, simple, complete, grammatically correct, and make sense in daily life conversations.".format(val)
print("input: " + llm_input)

list_grammar = r'''
root ::= "[" items "]" EOF

items ::= item ("," ws* item)*

item ::= string

string  ::=
  "\"" word (ws+ word)* "\"" ws*

word ::= [a-zA-Z]+

ws ::= " "

EOF ::= "\n"
'''

json_grammar = r'''
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

grammar = LlamaGrammar.from_string(list_grammar)
llm = Llama("zephyr-7b-beta.Q4_K_M.gguf",
            seed=-1,
            n_ctx=1024)

response = llm(
    llm_input,
    grammar=grammar,
    max_tokens=-1
)
print(response["choices"][0])
text_result = response["choices"][0]["text"]
data = json.loads(text_result)
print(json.dumps(data, indent=4))
