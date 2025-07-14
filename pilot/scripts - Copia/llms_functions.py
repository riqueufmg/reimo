import pandas as pd
import requests
import subprocess

API_URL = "https://otnk6c3y6fae8bgb.us-east-1.aws.endpoints.huggingface.cloud/v1/chat/completions"
API_TOKEN = "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"

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
        "max_tokens": 10000
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        choices = response_json.get("choices", [])
        if choices:
            content = choices[0].get("message", {}).get("content", "")
            print("Model output:\n")
            print(content)
            
            with open(f"outputs/output_{sample_id}.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print(f"\n'output_{sample_id}.txt' was created.")
        else:
            print("Output not found.")
    else:
        print(f"Request error: {response.status_code}")
        print(response.text)
    