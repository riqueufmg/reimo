from snippets_functions import get_samples, get_snippet, snippet_to_file, backup_original_class, replace_method, restore_original_class, build_repository, analyze_build_output
from llms_functions import hf_inference_endpoint, zeroshot_prompt
from parser_llm_output import extract_issue_description, extract_refactored_code, extract_refactoring_explanation
from dotenv import load_dotenv

import pandas as pd
import time
import os
import logging

load_dotenv()
API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/process.log")
    ]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    start_time = time.time()
    logger.info("Starting main execution")

    samples = get_samples('data/samples.csv', ',')
    logger.info(f"Loaded {len(samples)} samples")

    # Generate LLM outputs
    for sample in samples:
        try:
            snippet = get_snippet(sample['repository'] + sample['path'], sample['line'])
            snippet_to_file(snippet, sample['id'])

            prompt = zeroshot_prompt(code_snippet=snippet)
            hf_inference_endpoint(
                prompt=prompt,
                api_url=API_URL,
                api_token=API_TOKEN,
                sample_id=sample['id']
            )
            
        except Exception as e:
            logger.error(f"Error processing sample {sample['id']}: {e}")

    # Compile & Test LLMs outputs
    for sample in samples:
        try:
            directory_path = f"outputs/{MODEL_NAME}/"

            if not os.path.exists(f"{directory_path}/outputs/output_{sample['id']}.txt"):
                continue

            extract_issue_description(
                f"{directory_path}outputs",
                f"{directory_path}issues_description"
            )
            
            extract_refactored_code(
                f"{directory_path}outputs",
                f"{directory_path}refactorings"
            )
            
            extract_refactoring_explanation(
                f"{directory_path}outputs",
                f"{directory_path}explanation"
            )

            backup_original_class(sample['repository'] + sample['path'])
            replace_method(
                sample['repository'] + sample['path'],
                sample['line'],
                f"{directory_path}refactorings/refactored_code_{sample['id']}.java"
            )
            build_output = build_repository(sample['repository'])
            
            build_log_dir = os.path.join("logs", "builds")
            os.makedirs(build_log_dir, exist_ok=True)
            build_log_path = os.path.join(build_log_dir, f"build_output_{sample['id']}.log")
            with open(build_log_path, "w", encoding="utf-8") as f_log:
                f_log.write(build_output)
            logger.info(f"Build output saved to {build_log_path}")

            build_status = analyze_build_output(build_output)
            logger.info(f"Build analysis result: {build_status}")
            
            '''if(build_status == "SUCCESS"):
                ### START COMMIT AND ROLLBACK
                modified_file = sample['repository'] + sample['path']
                repo_path = sample['repository']

                commit_repository(modified_file, repo_path, sample['id'])

                # ... run RefactoringMiner ...

                rollback_commit(repo_path)
                ### END COMMIT AND ROLLBACK'''

            restore_original_class(sample['repository'] + sample['path'])

            build_output_2 = build_repository(sample['repository'])
            with open(build_log_path.replace(".log", "_restore.log"), "w", encoding="utf-8") as f_log2:
                f_log2.write(build_output_2)
            logger.info(f"Build output after restore saved to {build_log_path.replace('.log', '_restore.log')}")

            build_status_2 = analyze_build_output(build_output_2)
            logger.info(f"Build analysis result after restore: {build_status_2}")

        except Exception as e:
            logger.error(f"Error processing sample {sample['id']}: {e}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Execution finished in {elapsed_time:.2f} seconds")
    print(f"\nExecution time: {elapsed_time:.2f} seconds")