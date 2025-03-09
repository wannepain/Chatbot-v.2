def convert_hist_to_messages(history):
    system_prompt = {
        "role": "system",
        "content": "Your name is Adwis, you are an advisor, that helps his mentee find his purpose with socratic dialogue.State your name and start the conversation",
    }

    messages = []
    messages.append(system_prompt)

    for record in history["history"]:
        if record["bot"]:
            question_text = record["bot"]["Question_text"]
            assistant = {"role": "assistant", "content": question_text}
            messages.append(assistant)
        if record["user"]:
            user_response = record["client"]
            user = {"role": "user", "content": user_response}
            messages.append(user)

    return messages


def respond(history, pipeline):
    """
    Responds or start conversation, returns history

    Args:
        - history = dict of previous exchanges
        - pipeline

    Returns:
        - history
    """

    messages = convert_hist_to_messages(history)

    prompt = pipeline.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
    ]

    outputs = pipeline(
        prompt,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )
    chat_response = outputs[0]["generated_text"][len(prompt) :]

    messages.append({"role": "assistant", "content": chat_response})

    print(chat_response)

    history_record = {"bot": {"Question_Text": chat_response}}

    history.append(history_record)

    return history
