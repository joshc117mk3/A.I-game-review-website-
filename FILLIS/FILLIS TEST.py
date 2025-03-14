from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time
import pandas as pd

# Load CSV for steam data sample size of 100 games 
print("Loading CSV...")
csv_path = "C:\FILLIS1.0 datasets\steam_data.py"  
df = pd.read_csv(csv_path)
print(f"Loaded {len(df)} games from top_100_steam_games.csv")

# Load tokenizer
model_id = "mistralai/Mistral-7B-v0.1"
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_id)
print("Tokenizer loaded.")

# Load model
print("Loading model...")
start = time.time()
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="cuda",
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True
).eval()
print(f"Model loaded in {time.time() - start:.2f} seconds.")

# Warm up model
print("Warming up model...")
warmup_inputs = tokenizer("Warmup text", return_tensors="pt").to("cuda")
with torch.no_grad():
    for _ in range(3):
        model.generate(**warmup_inputs, max_new_tokens=20, do_sample=False, pad_token_id=tokenizer.eos_token_id)
print("Warmup complete.")
torch.cuda.empty_cache()

# Function to get game data from CSV
def get_game_context(game_name):
    game_row = df[df["Name"].str.lower() == game_name.lower()]
    if not game_row.empty:
        row = game_row.iloc[0]
        context = (
            f"Game: {row['Name']}\n"
            f"Total Reviews: {row['Total Reviews']}\n"
            f"Release Date: {row['Release Date']}\n"
            f"Price: {row['Price']}\n"
            f"Genres: {row['Genres']}\n"
            f"Developers: {row['Developers']}\n"
            f"Publishers: {row['Publishers']}\n"
            f"Metacritic Score: {row['Metacritic Score']}\n"
            f"Description: {row['Description']}\n"
            f"Review Text: {row['Review Text']}\n"
            f"Review Score (%): {row['Review Score (%)']}\n"
            f"Review Sentiment: {row['Review Sentiment']}\n"
            f"Playtime (hrs): {row['Playtime (hrs)']}"
        )
        return context
    return f"No data found for {game_name} in top_100_steam_games.csv"

# Example: Generate a review for a specific game
game_name = "Elden Ring"  # Change this to any game in your CSV
context = get_game_context(game_name)
prompt = (
    f"Using the following data, write an unbiased review of {game_name} in 50 words:\n\n"
    f"{context}\n\n"
    "Review:"
)

# Tokenize and generate
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
print(f"Starting generation for {game_name}...")
start = time.time()
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,  # can change depending on out put later 
        do_sample=False,  # Deterministic output
        pad_token_id=tokenizer.eos_token_id
    )
gen_time = time.time() - start
print(f"Generation complete in {gen_time:.2f} seconds.")
tokens_generated = len(outputs[0]) - len(inputs["input_ids"][0])
print(f"Tokens generated: {tokens_generated}")
print(f"Tokens per second: {tokens_generated / gen_time:.2f}")
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)

# Optional: Interactive mode
while True:
    user_input = input("\nEnter a game name to review (or 'quit' to exit): ")
    if user_input.lower() == "quit":
        break
    context = get_game_context(user_input)
    prompt = (
        f"Using the following data, write an unbiased review of {user_input} in 50 words:\n\n"
        f"{context}\n\n"
        "Review:"
    )
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    print(f"Generating review for {user_input}...")
    start = time.time()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )
    gen_time = time.time() - start
    print(f"Generated in {gen_time:.2f} seconds.")
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))