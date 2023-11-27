# flashcard_llm

# build docker image
```
docker build -t flashcard_llm .
```

# run docker image
```
docker run --rm -e AWS_LAMBDA_FUNCTION_TIMEOUT=900 -e AWS_LAMBDA_FUNCTION_MEMORY_SIZE=10240 -p 9000:8080 flashcard_llm:latest
```

# clean docker
```
docker system prune -f -a
```

# how to test function
```
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d {}
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"max_tokens": "1024", "prompt": "[\"hello\", \"good morning\", \"I\", \"like\", \"eat\", \"drink\", \"rice\", \"water\"]"}'
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"max_tokens": "1024", "prompt": "<s>[INST] <<SYS>> You are a helpful assistant. <</SYS>> What is a Large Language Model? [/INST]"}'
```

# examples
```
["kite", "lemon", "moon", "nest", "orange", "pencil", "queen", "rabbit", "sun", "tree"]
["umbrella", "violin", "whale", "xylophone", "yacht", "zebra", "window", "vase", "unicorn", "tiger"]
["star", "rain", "mountain", "lake", "island", "forest", "desert", "cloud", "beach", "valley"]
["chair", "table", "lamp", "sofa", "mirror", "drawer", "painting", "carpet", "pillow", "shelf"]
["banana", "cherry", "date", "fig", "grapefruit", "kiwi", "lime", "mango", "nectarine", "olive"]
["bread", "cheese", "egg", "fish", "garlic", "honey", "jam", "kale", "lettuce", "mushroom"]
["notebook", "eraser", "scissors", "glue", "tape", "ruler", "stapler", "pencil case", "marker", "clip"]
["bus", "car", "train", "plane", "bicycle", "scooter", "motorcycle", "boat", "subway", "tram"]
["happy", "sad", "angry", "excited", "tired", "scared", "bored", "surprised", "calm", "nervous"]
["run", "blue", "apple", "think", "happy", "chair", "sing", "quick", "mountain", "write"]
["jump", "red", "dog", "listen", "bright", "river", "dance", "soft", "book", "paint"]
["swim", "yellow", "tree", "speak", "cold", "cloud", "laugh", "smooth", "car", "draw"]
["walk", "green", "cat", "hear", "warm", "rain", "cry", "sharp", "house", "play"]
["climb", "orange", "flower", "see", "dark", "sun", "smile", "rough", "lamp", "cook"]
```
