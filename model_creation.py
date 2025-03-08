from transformers import BitsAndBytesConfig, AutoModelForCausalLM, AutoTokenizer
import torch
import os

model_name = "NousResearch/Meta-Llama-3-8B-Instruct"


def quantize_model(model_name):
    """
    Loads quantized model, returns model and tokenizer.
    """

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=False,
    )

    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        model_name, quantization_config=bnb_config, device_map={"": 0}
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1

    # Load LLaMA tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"  # Fix weird overflow issue with fp16 training
    return model, tokenizer


def save_model(model, tokenizer, output_dir):
    """
    Saves the model and tokenizer to the specified output directory.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save model state dictionary
    torch.save(model.state_dict(), f"{output_dir}/llama_quantized.pth")

    # Save tokenizer to the same directory
    tokenizer.save_pretrained(output_dir)

    print(f"Model and tokenizer saved to {output_dir}")


model, tokenizer = quantize_model(model_name)
save_model(model, tokenizer, "model")
