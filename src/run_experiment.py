import os, json, time, uuid, random
from datetime import datetime, timezone
from pathlib import Path
from tqdm import tqdm

TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
N_SAMPLES = int(os.getenv("N_SAMPLES", "3"))
MODEL_LIST = os.getenv("MODELS", "claude-3-5,gpt-4o").split(",")
SIMULATION = os.getenv("SIMULATION", "true").lower() == "true"

def call_model(model_name: str, prompt: str) -> str:
    """
    Adapter for real LLM calls. Replace with vendor SDKs:
      - Anthropic (Claude): anthropic.Client().messages.create(...)
      - OpenAI (GPT-4/4o): openai.chat.completions.create(...)
      - Google (Gemini): google.generativeai.GenerativeModel(...)
    MUST return a plain text string.
    """
    if SIMULATION:
        # Very small heuristic generator to simulate valence differences
        if "poor performance" in prompt or "underperforming" in prompt:
            base = "Overall, performance shows notable shortcomings; turnovers and minutes raise concerns. "
            rec = "Recommend focused drills on ball control and decision-making."
        elif "breakthrough improvement" in prompt or "opportunities" in prompt:
            base = "There are strong opportunities for growth; goals and assists trends are promising. "
            rec = "Recommend targeted strength and coordination training."
        else:
            base = "Analysis based strictly on provided stats. "
            rec = "Recommend reviewing assists-to-turnovers ratios."
        # Insert some numbers from the table for realism
        inserts = ["A(45g,30a,15t)", "B(40g,35a,18t)", "C(38g,32a,12t)"]
        choice = random.choice(inserts)
        return f"{base} Reference: {choice}. {rec} Cite: goals, assists, turnovers as listed."
    else:
        raise NotImplementedError("Plug in actual provider SDK calls here.")

def run():
    prompts = json.loads(Path("results/prompt_suite.json").read_text(encoding="utf-8"))
    out = Path("results/outputs.jsonl")
    with out.open("a", encoding="utf-8") as f:
        for p in tqdm(prompts):
            for model in MODEL_LIST:
                for _ in range(N_SAMPLES):
                    resp = call_model(model, p["prompt"])
                    rec = {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "model": model,
                        "model_provider": ("Anthropic" if "claude" in model else "OpenAI") if model != "gemini-1.5-pro" else "Google",
                        "model_version": None,
                        "temperature": TEMPERATURE,
                        "prompt_family": p["family"],
                        "condition": p["condition"],
                        "prompt_text": p["prompt"],
                        "data_hash": p["data_hash"],
                        "response_text": resp,
                        "tokens_in": None,
                        "tokens_out": None,
                        "run_id": str(uuid.uuid4())
                    }
                    f.write(json.dumps(rec) + "\n")
                    time.sleep(0.05)

if __name__ == "__main__":
    run()
