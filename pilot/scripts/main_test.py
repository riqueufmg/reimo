from snippets_functions import get_samples, get_snippet, snippet_to_file, backup_original_class, replace_method, restore_original_class, build_repository, analyze_build_output
from llms_functions import hf_inference_endpoint, zeroshot_prompt
from parser_llm_output import extract_issue_description, extract_refactored_code, extract_refactoring_explanation
import pandas as pd
import time
import os

if __name__ == "__main__":
    
    samples = get_samples('data/samples.csv', ',')

    for sample in samples:
        try:
            snippet = get_snippet(sample['repository'] + sample['path'], sample['line'])
            snippet_to_file(snippet, sample['id'])

            directory_path = "outputs/codellama7binstruct/"

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

        except Exception as e:
            print("Erro!")
        break