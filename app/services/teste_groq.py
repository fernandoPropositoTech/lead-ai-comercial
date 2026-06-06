from groq import Groq

client = Groq(
    api_key="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"
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "Olá"
        }
    ]
)

print(response.choices[0].message.content)