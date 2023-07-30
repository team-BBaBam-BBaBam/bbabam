import transformers

# TODO
device = "mps"

model = transformers.AutoModelForCausalLM.from_pretrained(
    "openlm-research/open_llama_7b_400bt_preview"
)

model.eval()
model.to(device)
print(f"Model loaded on {device}")
