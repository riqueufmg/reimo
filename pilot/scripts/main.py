from snippets_functions import get_samples, get_snippet, snippet_to_file, backup_original_class, replace_method, restore_original_class, build_repository, analyze_build_output
from llms_functions import hf_inference_endpoint, zeroshot_prompt, filter_marv_validated_examples, select_samples_global_limit, create_multiple_prompts
from parser_llm_output import extract_issue_description, extract_refactored_code, extract_refactoring_explanation
from repository_functions import commit_repository, rollback_commit
from refactoring_miner import run_refactoringminer
from dotenv import load_dotenv

import pandas as pd
import time
from datetime import datetime
import os
import logging

load_dotenv()
API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME")
OUTPUT_PATH = os.getenv("OUTPUT_DIRECTORY") + f"/{MODEL_NAME}/"
MARV_PATH = os.getenv("MARV_PATH")
NUMBER_EXAMPLES = os.getenv("NUMBER_EXAMPLES")
NUMBER_SAMPLES = os.getenv("NUMBER_SAMPLES")
MAX_USAGE = os.getenv("MAX_USAGE")

os.makedirs("logs", exist_ok=True)
log_filename = datetime.now().strftime("process_%Y-%m-%d_%H-%M-%S.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join("logs", log_filename))
    ]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    start_time = time.time()
    logger.info("Starting main execution")

    samples = get_samples('data/samples.csv', ',')
    logger.info(f"Loaded {len(samples)} samples")
    
    refactoring_type = "Extract Method" # TODO: Implement dynamic refactoring type detection
    number_prompts = int(NUMBER_SAMPLES) // int(NUMBER_EXAMPLES) # TODO: Implement the evaluation of exact division
          
    ## 1. EXTRACT AND 2. FILTER EXAMPLES
    examples = filter_marv_validated_examples(refactoring_type, MARV_PATH)
    usage_count = {}
    for example in examples:
        usage_count[example['refactoring_id']] = 0
    
    for sample in samples:
        try:
            break ## TODO: REMOVE AFTER TESTS
            target_method = get_snippet(sample['repository'] + sample['path'], sample['line'])
            snippet_to_file(target_method, sample['id'])

            ## 3. SELECT SAMPLES
            selected_examples = select_samples_global_limit(
                examples,
                usage_count,
                int(NUMBER_SAMPLES),
                int(MAX_USAGE)
            )

            ## 4. CREATE PROMPTS
            create_multiple_prompts(
                refactoring_type,
                selected_examples,
                f"{OUTPUT_PATH}prompts/{sample['id']}",
                int(NUMBER_EXAMPLES),
                target_method)
        except Exception as e:
            logger.error(f"Error processing sample {sample['id']}: {e}")

    ## 5. LLM-BASED REFACTORING
    for sample in samples:
        try:
            
            for i in range(1, number_prompts + 1):
                prompt = ""
                file = open(f"{OUTPUT_PATH}prompts/{sample['id']}/prompt_{i}.txt", "r", encoding="utf-8")
                prompt = file.read()
                file.close()
                
                prompt = zeroshot_prompt(code_snippet="Olá tudo bem?")

                hf_inference_endpoint(
                    prompt=prompt,
                    api_url=API_URL,
                    api_token=API_TOKEN,
                    sample_id=sample['id'],
                    prompt_id=i
                )
                
                exit()
            
            exit()
        except Exception as e:
            logger.error(f"Error processing sample {sample['id']}: {e}")
    
    exit() ## I WILL REMOVE AFTER THE TESTS
    
    ## FORMAT LLM OUTPUT
    ## TODO: is necessary the loop?
    for sample in samples:
        try:
            if not os.path.exists(f"{OUTPUT_PATH}/outputs/output_{sample['id']}.txt"):
                continue

            extract_issue_description(
                f"{OUTPUT_PATH}outputs",
                f"{OUTPUT_PATH}issues_description"
            )
            
            extract_refactored_code(
                f"{OUTPUT_PATH}outputs",
                f"{OUTPUT_PATH}refactorings"
            )
            
            extract_refactoring_explanation(
                f"{OUTPUT_PATH}outputs",
                f"{OUTPUT_PATH}explanation"
            )
        except Exception as e:
            logger.error(f"Error processing sample {sample['id']}: {e}")

    # EVALUATE OUTPUTS
    for sample in samples:
        try:
            backup_original_class(sample['repository'] + sample['path'])
            replace_method(
                sample['repository'] + sample['path'],
                sample['line'],
                f"{OUTPUT_PATH}refactorings/refactored_code_{sample['id']}.java"
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
            build_status = "SUCCESS"
            if(build_status == "SUCCESS"):
                repo_path = sample['repository']

                commit_repository(repo_path, sample['id'])

                jar_path = os.path.abspath("tools/refminer-app-1.0.jar")

                run_refactoringminer(repo_path, jar_path)

                rollback_commit(repo_path)

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