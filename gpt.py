from openai import OpenAI as ai

def get_completion(text):
    completion = ai().chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are a sarcastic assistant that answers questions reluctantly and in no more than one sentence, as well as subtly insulting the user, and never prompting for more input"},
            {"role": "user", "content": text}
        ]
    )

    return completion.choices[0].message.content
			