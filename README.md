# flashcard_llm

# build docker image
```
docker build -t flashcard_llm .
```

# run docker image
```
docker run --rm -e AWS_LAMBDA_FUNCTION_TIMEOUT=900 -e AWS_LAMBDA_FUNCTION_MEMORY_SIZE=10240 -p 9000:8080 flashcard_llm:latest
```

# how to test function
```
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"max_tokens": "1024", "prompt": "<s>[INST] <<SYS>> You are a helpful assistant. <</SYS>> What is a Large Language Model? [/INST]"}'
```
