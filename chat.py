import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

models = openai.Model.list()

for model in models.data:
    print("model => %s" % model.id)

model = 'gpt-3.5-turbo-16k-0613'


def chat_completion(messages):
    result = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    if result and result.choices[0]:
        choice = result.choices[0]
        return choice.message.content

    return None
