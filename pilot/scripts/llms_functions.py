import pandas as pd
import requests
import subprocess
import os
import logging
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
    