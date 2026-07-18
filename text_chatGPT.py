# Groq Ai
import secrets
import streamlit
from groq import Groq
client = Groq(api_key=st.secrets["api"]["key"])
prompt="Hello, how are you?"
completion = client.chat.completions.create(
  model="openai/gpt-oss-120b",
  messages=[
    {"role": "user", "content": prompt}
  ]
)

print(completion.choices[0].message.content)
