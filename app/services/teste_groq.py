from groq import Groq

from app.config.settings import GROQ_API_KEY


client = Groq(
    api_key=GROQ_API_KEY
)


response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Olá"
        }
    ]
)


print(
    response.choices[0].message.content
)