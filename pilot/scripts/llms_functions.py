import pandas as pd
import requests
import json
import random
import os
import logging
from transformers import AutoTokenizer

logger = logging.getLogger(__name__)

def zeroshot_prompt(code_snippet):
    
    template = """The following code snippet have high Cognitive Complexity. Refactor it using Extract Method.

    Code to be refactored:
    {code_snippet}

    Please identify the issue, refactor the code accordingly, and return the result strictly using the format below.

    Expected output:
    <issue identification>
    The description of the issue should be between these tags.
    </issue identification>
    <refactored code>
    The code after the refactoring should be between these tags.
    </refactored code>
    <refactoring explanation>
    The explanation of the refactoring should be between these tags.
    </refactoring explanation>
    """
    return template.format(code_snippet=code_snippet)

def filter_marv_validated_examples(refactoring_type, MaRV_path):
    try:
        refactorings = []

        with open(MaRV_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        extract_method_data = data.get(refactoring_type, [])

        df = pd.DataFrame(extract_method_data)

        for index, row in df.iterrows():
            sum = 0
            for vote in row.evaluations:
                sum += vote["vote"]
            
            if sum == 2:
                refactoring = {
                    "refactoring_id": row.refactoring_id,
                    "commit_sha": row.commit_sha,
                    "commit_link": row.commit_link,
                    "file_path": row.file_path,
                    "description": row.description,
                    "code_before": row.code_before,
                    "code_after": row.code_after
                }
                refactorings.append(refactoring)

        return refactorings
    
    except requests.RequestException as e:
        logger.error(f"Load MaRV examples failed: {e}")
        return

def select_samples_from_examples(examples, num_samples=15):
    if not examples:
        logger.warning("No examples available for sampling.")
        return []

    return random.sample(examples, min(num_samples, len(examples)))

def estimate_token_count(prompt):
    num_words = len(prompt.split())
    return int(num_words / 0.75)

def create_fewshot_prompt(samples):
    return 0

def create_cot_prompt():
    return 0

def create_fewshot_prompt(samples):
    if not samples:
        logger.warning("No samples provided for creating few-shot prompt.")
        return "", 0

    try:
        base_prompt = (
            "You are an expert in refactoring code snippets to reduce Cognitive Complexity. "
            "Below are some examples of refactoring using the Extract Method technique.\n\n"
        )

        for sample in samples:
            try:
                base_prompt += f"Refactoring ID: {sample['refactoring_id']}\n"
                base_prompt += f"Code Before:\n{sample['code_before']}\n"
                base_prompt += f"Code After:\n{sample['code_after']}\n"
                base_prompt += f"Issue Identification: {sample['description']}\n"
                base_prompt += "----------------------------------------\n"
            except KeyError as e:
                logger.error(f"Missing key in sample: {e}. Sample: {sample}")
                continue

        output_dir = "outputs/codellama7binstruct/prompts"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "fewshot_prompt.txt")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(base_prompt)
        logger.info(f"Few-shot prompt saved to '{output_path}'.")

        num_tokens = estimate_token_count(base_prompt)
        logger.info(f"Prompt contains approximately {num_tokens} tokens.")

        return base_prompt, num_tokens

    except Exception as e:
        logger.exception(f"Error while creating few-shot prompt: {e}")
        return "", 0

def hf_inference_endpoint(prompt, api_url, api_token, sample_id):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "tgi",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.0,
        "max_tokens": 2000
    }

    logger.info(f"Sending inference request for sample_id: {sample_id}")

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=data,
            timeout=(5, 300)
        )
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return

    response_json = response.json()
    choices = response_json.get("choices", [])

    if not choices:
        logger.warning("Output not found in response.")
        return

    content = choices[0].get("message", {}).get("content", "")
    logger.info("Model output received.")

    output_dir = "outputs/codellama7binstruct/outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"output_{sample_id}.txt")

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Output saved to '{output_path}'.")
    except Exception as e:
        logger.error(f"Failed to write output file '{output_path}': {e}")

refactoring_type = "Extract Method"
MaRV_path = "data/MaRV.json"

samples = select_samples_from_examples(filter_marv_validated_examples(refactoring_type, MaRV_path), num_samples=15)

prompt, tokens = create_fewshot_prompt(samples)

print(f"Few-shot prompt created with {tokens} tokens.")