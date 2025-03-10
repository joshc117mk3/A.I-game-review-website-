from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time

model_id = "mistralai/Mistral-7B-v0.1"
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_id)
print("Tokenizer loaded.")

print("Loading model...")
start = time.time()
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="cuda",
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True
).eval()
print(f"Model loaded in {time.time() - start:.2f} seconds.")

print("Warming up model...")
warmup_inputs = tokenizer("Warmup text", return_tensors="pt").to("cuda")
with torch.no_grad():
    for _ in range(3):
        model.generate(**warmup_inputs, max_new_tokens=20, do_sample=False, pad_token_id=tokenizer.eos_token_id)
print("Warmup complete.")
torch.cuda.empty_cache()

text = "Write an unbiased review of Elden Ring in 50 words."
inputs = tokenizer(text, return_tensors="pt").to("cuda")
print("Starting generation...")
start = time.time()
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=60,  # ~50 words
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )
gen_time = time.time() - start
print(f"Generation complete in {gen_time:.2f} seconds.")
print(f"Tokens generated: {len(outputs[0]) - len(inputs['input_ids'][0])}")
print(f"Tokens per second: {(len(outputs[0]) - len(inputs['input_ids'][0])) / gen_time:.2f}")
print(tokenizer.decode(outputs[0], skip_special_tokens=True))