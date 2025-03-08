from transformers import BitsAndBytesConfig, AutoModelForCausalLM, AutoTokenizer
import torch
import os


bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=False,
)


def load_model(model_name):
    """
    Loads quantized model, returns model and tokenizer.
    """
    # Load base model again
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,  # Use the same config
        device_map={"": 0},
    )

    # Load saved state_dict
    model.load_state_dict(torch.load("llama_quantized.pth"))

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained("llama_tokenizer")

    return model, tokenizer
