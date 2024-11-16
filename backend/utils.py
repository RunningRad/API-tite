from openai import OpenAI


client = OpenAI()

def get_response(q):

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer the questions the user asks."},
            {"role": "user", "content": q}
        ]   
    )
    return completion.choices[0].message.content

