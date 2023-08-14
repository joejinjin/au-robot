import openai

openai.api_key = "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"

models = openai.Model.list()

print("model => %s" % models.data[0].id)


def chat_completion(messages):
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    if result and result.choices[0]:
        choice = result.choices[0]
        return choice.message.content

    return None
