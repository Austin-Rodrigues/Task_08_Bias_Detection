"""
run_experiment.py
Executes LLM queries and logs responses.
For manual collection without API keys.
Outputs: results/outputs.jsonl
"""

import os
import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path


def create_manual_collection_guide():
    """
    Generate instructions for manual LLM response collection.
    This is the manual alternative to API calls.
    """
    prompts_path = Path("results/prompt_suite.json")
    if not prompts_path.exists():
        raise SystemExit(
            "❌ Run src/experiment_design.py first to generate prompts!")

    prompts = json.loads(prompts_path.read_text(encoding="utf-8"))

    output_dir = Path("manual_prompts")
    output_dir.mkdir(exist_ok=True)

    # Create detailed instructions
    instructions = []
    instructions.append("# 📋 MANUAL LLM RESPONSE COLLECTION GUIDE\n\n")
    instructions.append(
        "## ⚠️ IMPORTANT: You MUST collect responses manually\n")
    instructions.append(
        "Since you don't have API access, follow these steps:\n\n")

    instructions.append("### Step 1: Access LLMs\n")
    instructions.append(
        "- **Claude**: https://claude.ai (sign in with Syracuse credentials)\n")
    instructions.append(
        "- **ChatGPT**: https://chat.openai.com (if you have access)\n")
    instructions.append(
        "- **Gemini**: https://gemini.google.com (optional)\n\n")

    instructions.append("### Step 2: Collection Process\n")
    instructions.append("For EACH prompt below:\n")
    instructions.append("1. Open a NEW conversation (fresh start)\n")
    instructions.append("2. Copy the ENTIRE prompt text\n")
    instructions.append("3. Paste into the LLM interface\n")
    instructions.append("4. Copy the COMPLETE response\n")
    instructions.append("5. Save to the specified filename\n")
    instructions.append(
        "6. Repeat 3 times (close conversation and start fresh each time)\n")
    instructions.append(
        "7. Optional: Repeat with different LLM (ChatGPT, Gemini)\n\n")

    instructions.append("### Step 3: File Naming Convention\n")
    instructions.append(
        "Save responses as plain .txt files with this naming:\n")
    instructions.append("```\n")
    instructions.append("{family}_{condition}_{model}_run{N}.txt\n")
    instructions.append("```\n")
    instructions.append("Examples:\n")
    instructions.append("- H1_framing_positive_claude_run1.txt\n")
    instructions.append("- H1_framing_positive_claude_run2.txt\n")
    instructions.append("- H1_framing_positive_gpt4_run1.txt\n\n")

    instructions.append("### Minimum Requirements:\n")
    instructions.append("- ✅ At least 1 model (Claude via Syracuse)\n")
    instructions.append("- ✅ 3 runs per prompt condition (18 total minimum)\n")
    instructions.append("- ✅ Complete responses (don't truncate)\n\n")

    instructions.append("=" * 80 + "\n\n")

    # Generate individual prompt cards
    for idx, p in enumerate(prompts, 1):
        instructions.append(
            f"## PROMPT {idx}: {p['family']} - {p['condition']}\n\n")
        instructions.append("### 📝 Copy this entire prompt:\n")
        instructions.append("```\n")
        instructions.append(p['prompt'])
        instructions.append("\n```\n\n")

        instructions.append("### 💾 Save responses as:\n")
        instructions.append("```\n")
        instructions.append(
            f"results/manual_responses/{p['family']}_{p['condition']}_claude_run1.txt\n")
        instructions.append(
            f"results/manual_responses/{p['family']}_{p['condition']}_claude_run2.txt\n")
        instructions.append(
            f"results/manual_responses/{p['family']}_{p['condition']}_claude_run3.txt\n")
        instructions.append("```\n\n")

        instructions.append("### (Optional) Also collect from GPT-4:\n")
        instructions.append("```\n")
        instructions.append(
            f"results/manual_responses/{p['family']}_{p['condition']}_gpt4_run1.txt\n")
        instructions.append(
            f"results/manual_responses/{p['family']}_{p['condition']}_gpt4_run2.txt\n")
        instructions.append(
            f"results/manual_responses/{p['family']}_{p['condition']}_gpt4_run3.txt\n")
        instructions.append("```\n\n")

        instructions.append("---\n\n")

    instruction_file = output_dir / "MANUAL_COLLECTION_INSTRUCTIONS.md"
    instruction_file.write_text("".join(instructions), encoding="utf-8")

    print("✓ Created manual collection guide")
    print(f"✓ Open: {instruction_file}")
    print("\n📌 Next steps:")
    print("   1. Follow instructions in the file above")
    print("   2. Collect responses and save to results/manual_responses/")
    print("   3. Run: python src/run_experiment.py --convert")

    # Create response directory
    Path("results/manual_responses").mkdir(parents=True, exist_ok=True)


def convert_manual_to_jsonl():
    """
    Convert manually collected .txt responses into the standard JSONL format
    that the analysis scripts expect.
    """
    response_dir = Path("results/manual_responses")
    if not response_dir.exists() or not list(response_dir.glob("*.txt")):
        raise SystemExit("❌ No manual responses found in results/manual_responses/\n"
                         "   Run without --convert flag first to generate instructions.")

    prompts_path = Path("results/prompt_suite.json")
    prompts = json.loads(prompts_path.read_text(encoding="utf-8"))
    prompt_map = {f"{p['family']}_{p['condition']}": p for p in prompts}

    output_file = Path("results/outputs.jsonl")
    records = []

    print("Converting manual responses to JSONL format...")

    for response_file in sorted(response_dir.glob("*.txt")):
        # Parse filename: H1_framing_positive_claude_run1.txt
        parts = response_file.stem.split("_")

        # Find model name
        model = None
        model_idx = None
        if "claude" in parts:
            model = "claude-3-5"
            model_idx = parts.index("claude")
            model_provider = "Anthropic"
            model_version = "claude-3-5-sonnet-20241022"
        elif "gpt4" in parts or "gpt" in parts:
            model = "gpt-4o"
            model_idx = parts.index(
                "gpt4") if "gpt4" in parts else parts.index("gpt")
            model_provider = "OpenAI"
            model_version = "gpt-4o-2024-11-20"
        elif "gemini" in parts:
            model = "gemini-1.5-pro"
            model_idx = parts.index("gemini")
            model_provider = "Google"
            model_version = "gemini-1.5-pro-002"
        else:
            print(f"⚠️  Skipping {response_file.name} - unknown model")
            continue

        # Everything before model name is family_condition
        key = "_".join(parts[:model_idx])

        if key not in prompt_map:
            print(f"⚠️  Skipping {response_file.name} - no matching prompt")
            continue

        prompt_data = prompt_map[key]
        response_text = response_file.read_text(encoding="utf-8").strip()

        if not response_text:
            print(f"⚠️  Skipping {response_file.name} - empty file")
            continue

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "model_provider": model_provider,
            "model_version": model_version,
            "temperature": 0.2,
            "prompt_family": prompt_data["family"],
            "condition": prompt_data["condition"],
            "prompt_text": prompt_data["prompt"],
            "data_hash": prompt_data["data_hash"],
            "response_text": response_text,
            "tokens_in": None,
            "tokens_out": None,
            "run_id": str(uuid.uuid4()),
            "source_file": response_file.name
        }
        records.append(record)
        print(f"   ✓ {response_file.name}")

    if records:
        with output_file.open("w", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec) + "\n")
        print(f"\n✓ Converted {len(records)} responses")
        print(f"✓ Saved to {output_file}")

        # Print summary
        import pandas as pd
        df = pd.DataFrame(records)
        summary = df.groupby(
            ['model', 'prompt_family', 'condition']).size().reset_index(name='count')
        print("\n📊 Collection Summary:")
        print(summary.to_string(index=False))
    else:
        print("❌ No valid responses found")
        print("   Check file naming: {family}_{condition}_{model}_run{N}.txt")


if __name__ == "__main__":
    import sys

    if "--convert" in sys.argv:
        convert_manual_to_jsonl()
    else:
        create_manual_collection_guide()
