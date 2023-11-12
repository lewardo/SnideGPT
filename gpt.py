from decouple import config
from openai import OpenAI

client = OpenAI(
    api_key=config("OPENAI_API_KEY")
)

messages = [
    {"role": "system", "content": "You are a sarcastic assistant that answers questions reluctantly and in no more than one sentence, as well as subtly insulting the user, and never prompting for more input"},
]

def get_completion(text):
    messages.append({"role": "user", "content": text})

    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )

    messages.append({"role": "system", "content": completion.choices[0].message.content})

    return completion.choices[0].message.content
			