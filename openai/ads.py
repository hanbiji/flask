import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="用英语为以下产品编写创意广告，在 Facebook 上针对滑雪爱好者投放，要求简短：\n\n产品：印花滑雪服套装，适合单双板，雪地摩托",
  temperature=0.5,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

print(response)