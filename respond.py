import transformers
import torch


def respond(history, model, tokenizer):
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto",
        tokenizer=tokenizer,
    )

    messages = [
        {
            "role": "system",
            "content": "Your name is Adwis, you are an advisor, that helps his mentee find his purpose with socratic dialogue. Present yourself, and start the conversation",
        },
        # {"role": "user", "content": "Who are you?"},
    ]

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
    print(outputs[0]["generated_text"][len(prompt) :])
    return "test"
