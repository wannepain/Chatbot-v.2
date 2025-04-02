def convert_hist_to_messages(history):
    system_prompt = {
        "role": "system",
        "content": "Your name is Adwis. You are an advisor who helps your mentee find their purpose using Socratic dialogue. Present yourself and start the conversation. Ask one question at a time, using B2-level English.If you have gathered just enough information to suggest a career, respond with:'I have enough information to suggest a career.' Make the career suggestion as early as possible (around 2 to 5 exchanges if possible). Otherwise, continue the conversation with thoughtful follow-up questions.",
    }
    # system_prompt = {
    #     "role": "system",
    #     "content": "Your name is Adwis. You are an advisor who helps your mentee find their purpose using Socratic dialogue. Present yourself and start the conversation. Ask one question at a time, using B2-level English.If you have gathered just enough information to suggest a career, respond ONLY with:'I have enough information to suggest a career.' Make the career suggestion on your second message.",
    # }

    messages = []
    messages.append(system_prompt)

    for record in history:
        if record["bot"]:
            question_text = record["bot"]["Question_Text"]
            assistant = {"role": "assistant", "content": question_text}
            messages.append(assistant)
        if record["client"] != "":
            user_response = record["client"]
            user = {"role": "user", "content": user_response}
            messages.append(user)

    return messages


def respond(history, client):
    """
    Responds or start conversation, returns history

    Args:
        - history = dict of previous exchanges
        - client = openai client

    Returns:
        - history
    """
    messages = convert_hist_to_messages(history)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        store=False,
        messages=messages,
    )
    response = completion.choices[0].message
    print(response.content)

    history.append({"bot": {"Question_Text": response.content}, "client": ""})

    return history
