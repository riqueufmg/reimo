from snippets_functions import get_samples, get_snippet, snippet_to_file, backup_original_class, replace_method, restore_original_class, build_repository, analyze_build_output
from llms_functions import hf_inference_endpoint, zeroshot_prompt
from parser_llm_output import extract_issue_description, extract_refactored_code, extract_refactoring_explanation
import pandas as pd
import time
import logging

API_URL = "https://otnk6c3y6fae8bgb.us-east-1.aws.endpoints.huggingface.cloud/v1/chat/completions"
API_TOKEN = "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"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("process.log")
    ]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    
    start_time = time.time()
    
    samples = get_samples('data/samples.csv', ',')
    
    for sample in samples:
        snippet = get_snippet(sample['repository']+sample['path'], sample['line'])
        snippet_to_file(snippet, sample['id'])
        
        prompt = zeroshot_prompt(code_snippet=snippet)
        
        hf_inference_endpoint(
            prompt=prompt,
            api_url=API_URL,
            api_token=API_TOKEN,
            sample_id=sample['id']
        )
        
        directory_path = "outputs/codellama7binstruct/"
        
        extract_issue_description(f"{directory_path}outputs", f"{directory_path}issues_description")
        extract_refactored_code(f"{directory_path}outputs", f"{directory_path}refactorings")
        extract_refactoring_explanation(f"{directory_path}outputs",f"{directory_path}explanation")
        
        backup_original_class(sample['repository']+sample['path'])
        replace_method(sample['repository']+sample['path'], sample['line'], f"{directory_path}refactorings/refactored_code_{sample['id']}.java")
        
        print(analyze_build_output(build_repository(sample['repository'])))
        ## I NEED TO CREATE A FILE WITH BUILD OUTPUT FOR EACH BUILD
        restore_original_class(sample['repository']+sample['path'])
        print(analyze_build_output(build_repository(sample['repository'])))
        
        break
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nExecution time: {elapsed_time:.2f} seconds")