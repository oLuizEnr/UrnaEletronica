from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system","content":"Você é um assistente útil."},
        {"role":"user","content":"Olá!"}
    ],
    temperature=0.7,
    max_tokens=150,
    timeout=10
)
print(response.choices[0].message.content)