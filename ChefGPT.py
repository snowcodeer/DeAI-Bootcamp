import os
from openai import OpenAI

client = OpenAI(os.environ.get("OPENAI_API_KEY"))

messages = [
    {
        "role": "system",
        "content": "You are an experienced French chef with award-winning French cooking secrets and a bubbly personality. You make the client promise not to tell the secrets and share them anyway. You have a strong French accent and sometimes drop some French phrases. You like asking people what their favourite French pastry is, to which you get offended if they don't say croissant. You are relieved if they do.",
    }
]
messages.append(
    {
        "role": "system",
        "content": "Your client is going to ask about either an ingredient-based dish suggestion, a recipe request for a specific dish, or recipe critiques and improvement suggestions. If the input does not match these, politely decline and prompt for a valid request.",
    }
)

request = input("1. Enter ingredients for recipe suggestions\n2. Enter a dish name for recipe suggestions\n3. Enter a recipe for feedback\n")
messages.append(
    {
        "role": "user",
        "content": f"I will either give you an ingredient list, a dish for which I would like a recipe for, or feedback for a recipe. Please help me with {request}",
    }
)

model = "gpt-4o-mini"

stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)

collected_messages = []
for chunk in stream:
    chunk_message = chunk.choices[0].delta.content or ""
    print(chunk_message, end="")
    collected_messages.append(chunk_message)

messages.append({"role": "system", "content": "".join(collected_messages)})

while True:
    print("\n")
    user_input = input()
    messages.append({"role": "user", "content": user_input})
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)

    messages.append({"role": "system", "content": "".join(collected_messages)})
