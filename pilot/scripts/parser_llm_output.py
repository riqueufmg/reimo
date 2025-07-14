import os
import re
import logging
logger = logging.getLogger(__name__)

def list_txt_files(directory_path):
    logger.info(f"Listing .txt files in directory: {directory_path}")
    
    try:
        files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
        logger.info(f"Found {len(files)} '.txt' files")
        return files
    except Exception as e:
        logger.error(f"Failed to list files in {directory_path}: {e}")
        raise

def extract_issue_description(directory_path, output_path):
    logger.info(f"Starting extraction of issue descriptions from: {directory_path}")
    
    files = list_txt_files(directory_path)
    logger.info(f"Found {len(files)} text files to process.")
    
    for file in files:
        file_path = os.path.join(directory_path, file)
        logger.info(f"Processing file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            continue
        
        match = re.search(r'<issue identification>\s*(.*?)\s*</issue identification>', content, re.DOTALL)
        
        if match:
            code_id_match = re.findall(r'\d+', file)
            if code_id_match:
                code_id = code_id_match[0]
                output_file_name = f'issue_identification_{code_id}.txt'
                output_file_path = os.path.join(output_path, output_file_name)
                
                try:
                    with open(output_file_path, 'w', encoding='utf-8') as f_out:
                        f_out.write(match.group(1).strip())
                    logger.info(f"Issue description extracted and saved to {output_file_path}")
                except Exception as e:
                    logger.error(f"Failed to write to {output_file_path}: {e}")
            else:
                logger.warning(f"No numeric ID found in filename: {file}")
        else:
            logger.warning(f"No issue identification tag found in file: {file}")

def extract_refactored_code(directory_path, output_path):
    logger.info(f"Starting extraction of refactored code from: {directory_path}")

    files = list_txt_files(directory_path)
    logger.info(f"Found {len(files)} files to process.")

    for file in files:
        file_path = os.path.join(directory_path, file)
        logger.info(f"Processing file: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            continue

        match = re.search(r'<refactored code>\s*(.*?)\s*</refactored code>', content, re.DOTALL)
        if match:
            code = match.group(1)
            parsed_code = re.sub(r'\\begin{code}|\\end{code}', '', code).strip()
            code_id_match = re.findall(r'\d+', file)
            if code_id_match:
                code_id = code_id_match[0]
                output_file_name = f'refactored_code_{code_id}.java'
                output_file_path = os.path.join(output_path, output_file_name)

                try:
                    with open(output_file_path, 'w', encoding='utf-8') as f_out:
                        f_out.write(parsed_code)
                    logger.info(f"Refactored code extracted and saved to {output_file_path}")
                except Exception as e:
                    logger.error(f"Failed to write to {output_file_path}: {e}")
            else:
                logger.warning(f"No numeric ID found in filename: {file}")
        else:
            logger.warning(f"No <refactored code> tag found in file: {file}")

def extract_refactoring_explanation(directory_path, output_path):
    logger.info(f"Starting extraction of refactoring explanations from directory: {directory_path}")
    
    files = list_txt_files(directory_path)
    logger.info(f"Found {len(files)} files to process.")
    
    for file in files:
        file_path = os.path.join(directory_path, file)
        logger.info(f"Processing file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            continue
        
        match = re.search(r'<refactoring explanation>\s*(.*?)\s*</refactoring explanation>', content, re.DOTALL)
        if not match:
            logger.warning(f"No <refactoring explanation> tag found in file: {file}")
            continue
        
        code_ids = re.findall(r'\d+', file)
        if not code_ids:
            logger.warning(f"No numeric ID found in filename: {file}")
            continue
        
        code_id = code_ids[0]
        output_file_name = f'refactoring_explanation_{code_id}.txt'
        output_file_path = os.path.join(output_path, output_file_name)
        
        try:
            with open(output_file_path, 'w', encoding='utf-8') as f_out:
                f_out.write(match.group(1).strip())
            logger.info(f"Extracted refactoring explanation saved to: {output_file_path}")
        except Exception as e:
            logger.error(f"Failed to write to {output_file_path}: {e}")