from llama_cpp import Llama

llm = Llama(model_path="./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")
response = llm("Скажи шутку на русском языке", max_tokens=50)
print(response["choices"][0]["text"])