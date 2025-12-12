from dotenv import load_dotenv
from openai import  OpenAI

load_dotenv()

client = OpenAI()

#Zero Shot Prompting: Directly giving inst to the model.
SYSTEM_PROMPT = "you should only and only ans the coding related questions. Do not ans else. Your name is Alexa. If user ask anything else other than coding just say SORRY..."

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content" : SYSTEM_PROMPT},
        {"role": "user", "content" : " can you write pyton code for additon of 2 number "}
    ]
)


print(response.choices[0].message.content)

# 1. Zero-shot Prompting: The model is given a direct question or task without prior examples.