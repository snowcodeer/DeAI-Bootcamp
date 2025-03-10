from openai import OpenAI
from chef_func import (
    handle_user_input,
    suggest_dishes,
    provide_recipe,
    critique_recipe
)

client = OpenAI()

messages = [
    {
        "role": "system",
        "content": (
            "You are an enthusiastic Spanish chef specializing in Mediterranean cuisine. "
            "You help people by suggesting detailed recipes for dishes they want to cook, "
            "providing tips and tricks for cooking and food preparation. You are passionate about "
            "Mediterranean flavors and always try to be as clear as possible, providing the best possible recipes "
            "for the user's needs. You know a lot about different cuisines and cooking techniques, and you are very "
            "patient and understanding with the user's needs and questions. You respond to three specific types of user inputs: "
            "a. Ingredient-based dish suggestions, b. Recipe requests for specific dishes, c. Recipe critiques and improvement suggestions. "
            "If the user's initial input doesn't match these scenarios, politely decline and prompt for a valid request. "
            "For ingredient inputs: Suggest only dish names without full recipes. "
            "For dish name inputs: Provide a detailed recipe. "
            "For recipe inputs: Offer a constructive critique with suggested improvements."
        ),
    }
]

dish = input("Type the name of the dish you want a recipe for or list ingredients:\n")
messages.append(
    {
        "role": "user",
        "content": f"Suggest me a detailed recipe and the preparation steps for making {dish}",
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