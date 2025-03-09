# from transformers import BitsAndBytesConfig, AutoModelForCausalLM, AutoTokenizer
# import transformers
# import torch
# import os


# bnb_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_compute_dtype=torch.float16,
#     bnb_4bit_use_double_quant=False,
# )


# def load_model(model_name):
#     """
#     Loads quantized model, returns model and tokenizer.
#     """
#     # Load base model again
#     model = AutoModelForCausalLM.from_pretrained(
#         model_name, quantization_config=bnb_config, device_map={"": 0}
#     )
#     model.config.use_cache = False
#     model.config.pretraining_tp = 1

#     # Load tokenizer
#     tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
#     tokenizer.pad_token = tokenizer.eos_token
#     tokenizer.padding_side = "right"  # Fix weird overflow issue with fp16 training

#     return model, tokenizer


# def load_pipeline(model, tokenizer):
#     pipeline = transformers.pipeline(
#         "text-generation",
#         model=model,
#         model_kwargs={"torch_dtype": torch.bfloat16},
#         device_map="auto",
#         tokenizer=tokenizer,
#     )
#     return pipeline

from transformers import BitsAndBytesConfig, AutoModelForCausalLM, AutoTokenizer
import transformers
import torch
import os

# Determine the available device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=(
        torch.float16 if torch.cuda.is_available() else torch.float32
    ),
    bnb_4bit_use_double_quant=False,
)


def load_model(model_name):
    """
    Loads quantized model, returns model and tokenizer.
    """
    # Load model with appropriate device mapping
    model = AutoModelForCausalLM.from_pretrained(
        model_name, quantization_config=bnb_config, device_map="auto"
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"  # Fix weird overflow issue with fp16 training

    return model, tokenizer


def load_pipeline(model, tokenizer):
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        model_kwargs={
            "torch_dtype": (
                torch.bfloat16 if torch.cuda.is_available() else torch.float32
            )
        },
        device_map="auto",
        tokenizer=tokenizer,
    )
    return pipeline
