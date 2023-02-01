import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = "ski jacket 在 amazon.com有哪些相关词?"
response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0.5,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
print('问: %s' % prompt)
print(response)