def gpt_summarize_history(history, client):
    """
    Uses GPT to generate a natural language summary of the conversation history focused on acitons.
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
            "content": "You are a summarizer. Create a 2-3 sentence summary of the use's conversation history. Focus on actions the user should take. Also include what they like and enjoy doing.",
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


def check_up(history, client):
    """
    Generates a check-up message based on the conversation history.
    """

    summarized_history = gpt_summarize_history(history, client)
    print(f"Summarized history: {summarized_history}")

    system_prompt = {
        "role": "system",
        "content": (
            "You are an accountability bot. "
            "You are here to help the user stay on track with their goals. "
            "You will ask the user about their progress. "
            "You will be provided wuth a summary of the conversation history. "
            "Focus on the career direction and purpose. "
            "Keep yout response as short as possible and to the point. Max 1 short question. 5-8 words. "
            "Your message will be used as a push notification. "
        ),
    }
    messages = [
        system_prompt,
        {"role": "system", "content": f"conversation summary: {summarized_history}"},
    ]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        store=False,
        messages=messages,
        max_tokens=100,  # Very small output
    )
    response = completion.choices[0].message
    print(response.content)

    return response.content.strip()
