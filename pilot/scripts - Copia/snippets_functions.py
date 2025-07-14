import pandas as pd
import subprocess
import time

def get_samples(path, delim):
    df = pd.read_csv(path, delimiter=delim)
    return df.to_dict(orient='records')

def get_snippet(path, line):
    result = subprocess.run(
        ['java', '-jar', 'tools/method-toolkit-1.0.jar', 'extract', path, str(line)],
        capture_output=True,
        text=True
    )
    return result.stdout

def backup_original_class(path):
    result = subprocess.run(
        ['java', '-jar', 'tools/method-toolkit-1.0.jar', 'backup', path],
        capture_output=True,
        text=True
    )
    return result.stdout

def replace_method(path, line, refactored_snippet_path):
    result = subprocess.run(
        ['java', '-jar', 'tools/method-toolkit-1.0.jar', 'replace', path, str(line), refactored_snippet_path],
        capture_output=True,
        text=True
    )
    return result.stdout

def restore_original_class(path):
    result = subprocess.run(
        ['java', '-jar', 'tools/method-toolkit-1.0.jar', 'restore', path],
        capture_output=True,
        text=True
    )
    return result.stdout

def snippet_to_file(snippet, id):
    file = open(f"outputs/snippets/code_{id}.java", "w", encoding="utf-8")
    
    try:
        file.write(snippet)
    finally:
        file.close()

def build_repository(repository_path):
    result = subprocess.run(
        ['mvn', 'clean', 'install', '-Dcheckstyle.skip=true'],
        capture_output=True,
        text=True,
        shell=True,
        cwd=repository_path
    )
    return result.stdout

def analyze_build_output(output):
    if "BUILD SUCCESS" in output:
        return "SUCCESS"
    elif "COMPILATION ERROR" in output:
        return "COMPILATION_ERROR"
    elif "There are test failures" in output or "Tests run:" in output and "Failures:" in output:
        return "TEST_FAILURE"
    elif "BUILD FAILURE" in output:
        return "UNKNOWN_FAILURE"
    else:
        return "UNKNOWN"
