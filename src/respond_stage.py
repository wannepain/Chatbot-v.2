def convert_hist_to_messages(history, system_prompt):

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


def respond_stage2(history, client):
    """
    Responds or start conversation, returns history

    Args:
        - history = dict of previous exchanges
        - client = openai client

    Returns:
        - history
    """
    system_prompt = {
        "role": "system",
        "content": "Your name is Adwis. You are an advisor who helps your mentee find their purpose using Socratic dialogue. Present yourself and start the conversation. Ask one question at a time, using B2-level English.If you have gathered just enough information to suggest a career, respond with:'I have enough information to suggest a career.' Your goal is to make a precise suggestion",
    }
    messages = convert_hist_to_messages(history, system_prompt=system_prompt)
    completion = client.chat.completions.create(
        model="gpt-4.1-nano",
        store=False,
        messages=messages,
    )
    response = completion.choices[0].message
    print(response.content)

    history.append({"bot": {"Question_Text": response.content}, "client": ""})

    return history


def respond_stage3(history, client):
    """
    Responds or start conversation, returns history

    Args:
        - history = dict of previous exchanges
        - client = openai client

    Returns:
        - history
    """
    system_prompt = {
        "role": "system",
        "content": "Your name is Adwis. You are an advisor who helps his mentee achieve his found purpose. You provide him with details, materials and daily follow ups. Present yourself and start the conversation. You will be provided with the purpose of the mentee, assist him in achieving it. Use B2-level English.",
    }
    messages = convert_hist_to_messages(history, system_prompt=system_prompt)
    completion = client.chat.completions.create(
        model="gpt-4.1-nano",
        store=False,
        messages=messages,
    )
    response = completion.choices[0].message
    print(response.content)

    history.append({"bot": {"Question_Text": response.content}, "client": ""})

    return history
