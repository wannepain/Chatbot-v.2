import json


def evaluate(history, client):
    format_example = json.dumps(
        {
            "Career_Name": "career name",
            "Description": "short description",
            "Starting_Salary": 10000,
        }
    )

    system_prompt = {
        "role": "system",
        "content": f"You are provided with a conversation between a mentor and a mentee. The mentor is trying to help the mentee find his purpose. You should find the career that the mentee is made for. Return the career name, short description, and average salary in USD in this JSON format: {format_example}",
    }
    user_prompt = {
        "role": "user",
        "content": f"What career is the mentee made for? Conversation: {history}",
    }

    messages = [system_prompt, user_prompt]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    response = completion.choices[0].message.content  # Extract text content

    try:
        final = json.loads(response)  # Attempt to parse as JSON
        print(final)
        return final
    except json.JSONDecodeError:
        print("Error: Response is not valid JSON.")
        print(response)  # Print raw response for debugging
        return None  # Indicate failure
