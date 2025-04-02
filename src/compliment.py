import json


def compliment(history, client):
    example_compliment = json.dumps(
        {
            "compliment": "You think like an innovator",
        }
    )

    system_prompt = {
        "role": "system",
        "content": f"You are provided with a conversation history, your task is to generate a compliment for the client based on the conversation. The compliment should be positive and encouraging. The compliment should be in the format of a JSON object with a single key 'compliment' and the value being the compliment. For example {example_compliment}. The compliment should be relevant to the conversation and should not be generic. It must be shorter than 7 words and emotional.",
    }
    user_prompt = {
        "role": "user",
        "content": f"Generate a compliment based on this conversation: {history}",
    }

    messages = [system_prompt, user_prompt]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        response_format={"type": "json_object"},
    )

    response = completion.choices[0].message.content  # Extract text content

    try:
        final = json.loads(response)  # Attempt to parse as JSON
        print(final)
        return final["compliment"]
    except json.JSONDecodeError:
        print("Error: Response is not valid JSON.")
        print(response)  # Print raw response for debugging
        return None  # Indicate failure
