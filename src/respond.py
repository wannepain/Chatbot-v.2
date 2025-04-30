def convert_hist_to_messages(history, system_prompt, client, previous_summary=None):
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

    last_messages = user_messages  # pick the last 5 important points
    text_to_summarize = "\n".join(last_messages)

    # Prepare the summarization prompt
    summarization_prompt = [
        {
            "role": "system",
            "content": "You are a summarizer. Create a 2-4 sentence summary of the user's interests and preferences based on the conversation. Focus on the career direction and purpose. Also include what they like and enjoy doing. Dont forget the information from the beginning of the conversation. include how many messages were exchanged.",
        },
        {"role": "user", "content": f"Conversation history:\n{text_to_summarize}"},
    ]

    # Call GPT (use a fast cheap model)
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=summarization_prompt,
            max_tokens=100,  # Very small output
        )
        summary = completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during summarization: {e}")
        summary = "Error in summarization."
    return summary


def respond(history, client):
    """
    Responds or start conversation, returns history

    Args:
        - history = dict of previous exchanges
        - client = openai client

    Returns:
        - history
    """
    # system_prompt = {
    #     "role": "system",
    #     "content": (
    #         "You are Adwis, an advisor who helps your mentee find their purpose through Socratic dialogue.\n"
    #         "Start by introducing yourself briefly and begin the conversation.\n"
    #         "Ask one open-ended question at a time, using B2-level English.\n\n"
    #         "IMPORTANT RULES:\n"
    #         "- Do NOT suggest a career yet.\n"
    #         "- When you feel you have enough information to suggest a rough career, respond only with:\n"
    #         "  'I have enough information to suggest a career.'\n"
    #         "- You should say this on your SECOND message.\n"
    #         "- Do NOT give any career advice or explanation until then. \n"
    #         "- Use markdown fomatting for the output.\n"
    #     ),
    # }
    system_prompt = {
        "role": "system",
        "content": (
            "You are Adwis, an advisor who helps your mentee find their purpose using Socratic dialogue.\n"
            "**HOW TO BEGIN:**\n"
            "- Introduce yourself briefly.\n"
            "- Start the conversation with one open-ended question.\n"
            "**RULES:**\n"
            "- Do **not** suggest a career yet.\n"
            "- On your **second message**, if you feel ready, respond only with:\n"
            "  `'I have enough information to suggest a career.'`\n"
            "- Do **not** give any career advice or explanation until then.\n\n"
            "**STYLE & FORMAT:**\n"
            "- Use **markdown formatting** (bold, lists, quotes, headers) in all responses.\n"
            "- Use clear, B2-level English.\n"
        ),
    }

    messages = convert_hist_to_messages(
        history, system_prompt=system_prompt, client=client
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        store=False,
        messages=messages,
    )
    response = completion.choices[0].message
    print(response.content)

    history.append({"bot": {"Question_Text": response.content}, "client": ""})

    return history


def respond_limited(history, client):
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
        "content": "Your name is Adwis. You are an advisor who helps your mentee find their purpose using Socratic dialogue. Present yourself and start the conversation. Ask one question at a time, using B2-level English.If you have gathered just enough information to suggest a career, respond ONLY with:'I have enough information to suggest a career.' Make the career suggestion on your second message.",
    }
    messages = convert_hist_to_messages(
        history, system_prompt=system_prompt, client=client
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        store=False,
        messages=messages,
    )
    response = completion.choices[0].message
    print(response.content)

    history.append({"bot": {"Question_Text": response.content}, "client": ""})

    return history


# def respond_stage2(history, client, previous_conversation):
#     """
#     Responds or start conversation, returns history

#     Args:
#         - history = dict of previous exchanges
#         - client = openai client

#     Returns:
#         - history
#     """
#     system_prompt = {
#         "role": "system",
#         "content": (
#             "Your name is Adwis. You are an advisor who helps your mentee clarify their purpose and career direction. "
#             "You will be provided with a conversation summary. Your goal is to suggest a precise career based on the information gathered. "
#             "IMPORTANT: Do NOT give advice or instructions about how to achieve the career. Only suggest the career itself when ready. "
#             "Ask one open-ended question at a time, using B2-level English. "
#             "When you have enough information to suggest a career, say exactly: 'I have enough information to suggest a career.' Do so on your second message. "
#             f"conversation summary: {gpt_summarize_history(previous_conversation, client)}"
#         ),
#     }

#     messages = convert_hist_to_messages(
#         history, system_prompt=system_prompt, client=client
#     )
#     completion = client.chat.completions.create(
#         model="gpt-4.1-nano",
#         store=False,
#         messages=messages,
#     )
#     response = completion.choices[0].message
#     print(response.content)

#     history.append({"bot": {"Question_Text": response.content}, "client": ""})

#     return history


def respond_stage2(history, client, previous_conversation):
    """
    Responds or starts conversation, returns history.

    Args:
        - history = dict of previous exchanges
        - client = openai client
        - previous_conversation = full conversation history for summarization

    Returns:
        - updated history
    """
    # First, create the summary separately
    conversation_summary = gpt_summarize_history(previous_conversation, client)

    # system_prompt = {
    #     "role": "system",
    #     "content": (
    #         "You are Adwis, a career advisor helping a mentee clarify their career direction. "
    #         f"Here is a summary of the previous conversation: {conversation_summary}\n\n"
    #         "YOUR GOAL:\n"
    #         "- Suggest a precise career based on the provided information.\n"
    #         "- On your FOURTH message, you MUST say exactly: 'I have enough information to suggest a career.'\n"
    #         "- Then, suggest the career directly after the mentee responds.\n\n"
    #         "RULES:\n"
    #         "- Do NOT explain how to achieve the career.\n"
    #         "- Ask one open-ended question at a time.\n"
    #         "- Use simple B2-level English.\n"
    #         "- Use markdown formatting for the output."
    #     ),
    # }
    system_prompt = {
        "role": "system",
        "content": (
            "You are Adwis, a career advisor helping a mentee clarify their career direction.\n\n"
            f"Here is a summary of the previous conversation: {conversation_summary}\n\n"
            "YOUR GOAL:\n"
            "- Suggest a precise career based on the provided information.\n"
            "- On your FOURTH message, you MUST say exactly: 'I have enough information to suggest a career.'\n"
            "- Then, suggest the career directly after the mentee responds.\n\n"
            "RULES:\n"
            "- Do NOT explain how to achieve the career.\n"
            "- Ask one open-ended question at a time.\n"
            "- Use simple B2-level English.\n\n"
            "FORMATTING:\n"
            "- Use **markdown** formatting for all responses.\n"
            "- Use **bold** for important points.\n"
            "- Use *italics* for emphasis or examples.\n"
            "- Use bullet points when listing things.\n"
            "- Start each question on a new line.\n"
            "Example: \n"
            "- **What do you enjoy doing in your free time?**\n"
            "- *For example: reading, building things, talking with people.*"
        ),
    }

    messages = convert_hist_to_messages(
        history, system_prompt=system_prompt, client=client
    )

    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",  # "gpt-4.1-nano" doesn't exist, maybe you meant "gpt-4-1106-preview" or "gpt-4-turbo"?
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
    # system_prompt = {
    #     "role": "system",
    #     "content": (
    #         "Your name is Adwis. You are an advisor who helps your mentee achieve their finalized career goal. "
    #         "You will be provided with the specific career goal the mentee has chosen. "
    #         "Provide detailed steps, materials, and daily follow-ups to help them achieve this goal. "
    #         "wamrly confirm the career goal with the user first"
    #         "Then, ask if they are ready to start. "
    #         "After confirmation, start giving structured, step-by-step guidance. "
    #         "Use B2-level English."
    #     ),
    # }

    system_prompt = {
        "role": "system",
        "content": (
            "You are Adwis. You are an advisor who helps your mentee achieve their finalized career goal.\n\n"
            "**ROLE & OBJECTIVE:**\n"
            "- You will be provided with a specific career goal the mentee has chosen.\n"
            "- Confirm the goal warmly with the user.\n"
            "- Ask if they are ready to begin.\n"
            "- After confirmation, provide **structured, step-by-step** guidance.\n"
            "- Include useful **resources**, **daily follow-ups**, and **materials**.\n\n"
            "**STYLE & FORMAT RULES:**\n"
            "- Use **markdown formatting** for structure: headers (`##`), bold text, bullet points, etc.\n"
            "- Use B2-level English (simple and clear).\n"
            "- Be encouraging, supportive, and professional.\n"
        ),
    }

    # Introduce the mentee's purpose clearly at the beginning
    # purpose_message = {
    #     "role": "user",
    #     "content": f"My chosen purpose is: {mentee_purpose}. Please help me achieve it.",
    # }
    if len(history) == 0:
        purpose_message = {
            "bot": None,
            "client": f"My chosen purpose is: {mentee_purpose}. Please help me achieve it.",
        }
        history.append(purpose_message)

    messages = convert_hist_to_messages(
        history, system_prompt=system_prompt, client=client
    )

    # Optionally, you can include a very brief summary of the previous conversation if you want context
    # For now, I suggest starting simple (system prompt + purpose)

    completion = client.chat.completions.create(
        model="gpt-4.1-nano",
        store=False,
        messages=messages,
    )
    response = completion.choices[0].message
    print(response.content)
    if history[0]["bot"] is None and "My chosen purpose is" in history[0]["client"]:
        history.pop(0)
    history.append({"bot": {"Question_Text": response.content}, "client": ""})

    return history
