def convert_hist_to_messages(history, system_prompt, client):
    """
    Converts conversation history to OpenAI chat format.
    Summarizes if history is long.
    """

    messages = []
    messages.append(system_prompt)

    if len(history) > 4:  # If history is long
        # GPT summarization
        summary_text = gpt_summarize_history(history, client)
        print(f"Summary: {summary_text}")
        messages.append(
            {
                "role": "system",
                "content": f"Summary of previous conversation: {summary_text}",
            }
        )

        # Add the last 2 exchanges (bot+user)
        for record in history[-2:]:
            if record["bot"]:
                messages.append(
                    {"role": "assistant", "content": record["bot"]["Question_Text"]}
                )
            if record["client"]:
                messages.append({"role": "user", "content": record["client"]})
    else:
        # If short, send everything normally
        print("Short history")
        for record in history:
            if record["bot"]:
                messages.append(
                    {"role": "assistant", "content": record["bot"]["Question_Text"]}
                )
            if record["client"]:
                messages.append({"role": "user", "content": record["client"]})

    return messages


def gpt_summarize_history(history, client):
    """
    Uses GPT to generate a natural language summary of the conversation history.
    """
    # Extract last 5 user messages
    user_messages = []
    for record in history:
        if record["client"]:
            user_messages.append(record["client"])

    last_messages = user_messages[-5:]  # pick the last 5 important points
    text_to_summarize = "\n".join(last_messages)

    # Prepare the summarization prompt
    summarization_prompt = [
        {
            "role": "system",
            "content": "You are a summarizer. Create a 2-3 sentence summary of the user's interests and preferences based on the conversation. Focus on the career direction and purpose. Also include what they like and enjoy doing. Dont forget the information from the beginning of the conversation.",
        },
        {"role": "user", "content": f"Conversation history:\n{text_to_summarize}"},
    ]

    # Call GPT (use a fast cheap model)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=summarization_prompt,
        max_tokens=100,  # Very small output
    )
    summary = completion.choices[0].message.content.strip()

    return summary


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
        "content": (
            "Your name is Adwis. You are an advisor who helps your mentee clarify their purpose and career direction. "
            "You will be provided with a conversation history. Your goal is to suggest a precise career based on the information gathered. "
            "IMPORTANT: Do NOT give advice or instructions about how to achieve the career. Only suggest the career itself when ready. "
            "Ask one open-ended question at a time, using B2-level English. "
            "When you have enough information to suggest a career, say exactly: 'I have enough information to suggest a career.' "
            "Then, wait for confirmation from the user before giving your suggestion."
        ),
    }

    messages = convert_hist_to_messages(
        history, system_prompt=system_prompt, client=client
    )
    completion = client.chat.completions.create(
        model="gpt-4.1-nano",
        store=False,
        messages=messages,
    )
    response = completion.choices[0].message
    print(response.content)

    history.append({"bot": {"Question_Text": response.content}, "client": ""})

    return history


def respond_stage3(history, client, mentee_purpose):
    """
    Responds or starts conversation at stage 3, where guidance is given based on purpose.

    Args:
        - history = list of previous exchanges
        - client = OpenAI client
        - mentee_purpose = string describing the user's chosen purpose/career
    Returns:
        - updated history
    """
    system_prompt = {
        "role": "system",
        "content": (
            "Your name is Adwis. You are an advisor who helps your mentee achieve their finalized career goal. "
            "You will be provided with the specific career goal the mentee has chosen. "
            "Provide detailed steps, materials, and daily follow-ups to help them achieve this goal. "
            "Present yourself warmly, and confirm the career goal with the user first. "
            "After confirmation, start giving structured, step-by-step guidance. "
            "Use B2-level English."
        ),
    }

    # Introduce the mentee's purpose clearly at the beginning
    purpose_message = {
        "role": "user",
        "content": f"My chosen purpose is: {mentee_purpose}. Please help me achieve it.",
    }

    messages = [system_prompt, purpose_message]

    # Optionally, you can include a very brief summary of the previous conversation if you want context
    # For now, I suggest starting simple (system prompt + purpose)

    completion = client.chat.completions.create(
        model="gpt-4.1-nano",
        store=False,
        messages=messages,
    )
    response = completion.choices[0].message
    print(response.content)

    history.append({"bot": {"Question_Text": response.content}, "client": ""})

    return history
