import os
import re

def list_txt_files(directory_path):
    files = []
    
    for f in os.listdir(directory_path):
        if f.endswith('.txt'):
            files.append(f)
        
    return files

def extract_issue_description(directory_path, output_path):
    files = list_txt_files(directory_path)
    
    for file in files:
        with open(os.path.join(directory_path, file), 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        match = re.search(r'<issue identification>\s*(.*?)\s*</issue identification>', conteudo, re.DOTALL)
        
        if match:
            code_id = re.findall(r'\d+', file)[0]
            file_name = f'issue_identification_{code_id}.txt'
            with open(os.path.join(output_path, file_name), 'w', encoding='utf-8') as f_out:
                f_out.write(match.group(1).strip())


def extract_refactored_code(directory_path, output_path):
    
    files = list_txt_files(directory_path)
    for file in files:
        with open(os.path.join(directory_path, file), 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'<refactored code>\s*(.*?)\s*</refactored code>', content, re.DOTALL)
        if match:
            code = match.group(1)
            parsed_code = re.sub(r'\\begin{code}|\\end{code}', '', code).strip()
            code_id = re.findall(r'\d+', file)[0]
            file_name = f'refactored_code_{code_id}.java'
            with open(os.path.join(output_path, file_name), 'w', encoding='utf-8') as f_out:
                f_out.write(parsed_code)


def extract_refactoring_explanation(directory_path,output_path):
    files = list_txt_files(directory_path)
    for file in files:
        with open(os.path.join(directory_path, file), 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'<refactoring explanation>\s*(.*?)\s*</refactoring explanation>', content, re.DOTALL)
        if match:
            code_id = re.findall(r'\d+', file)[0]
            file_name = f'refactoring_explanation_{code_id}.txt'
            with open(os.path.join(output_path, file_name), 'w', encoding='utf-8') as f_out:
                f_out.write(match.group(1).strip())