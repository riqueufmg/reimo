import pandas as pd
import subprocess
import time
import os
import logging
logger = logging.getLogger(__name__)

def get_samples(path, delim):
    logger.info(f"Reading samples from: {path} with delimiter: '{delim}'")
    try:
        df = pd.read_csv(path, delimiter=delim)
        logger.info(f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns")
        return df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Failed to read samples from {path}: {e}")
        raise

def get_snippet(path, line):
    logger.info(f"Extracting snippet from file: {path} at line: {line}")

    try:
        result = subprocess.run(
            ['java', '-jar', 'tools/method-toolkit-1.0.jar', 'extract', path, str(line)],
            capture_output=True,
            text=True,
            check=True  # levanta CalledProcessError se falhar
        )
        logger.info("Snippet extraction completed successfully.")
        return result.stdout

    except subprocess.CalledProcessError as e:
        logger.error(f"Snippet extraction failed: {e}. STDERR: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during snippet extraction: {e}")
        raise

def backup_original_class(path):
    logger.info(f"Creating backup for class file: {path}")

    try:
        result = subprocess.run(
            ['java', '-jar', 'tools/method-toolkit-1.0.jar', 'backup', path],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info("Backup completed successfully.")
        return result.stdout

    except subprocess.CalledProcessError as e:
        logger.error(f"Backup failed for {path}: {e}. STDERR: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during backup for {path}: {e}")
        raise

def replace_method(path, line, refactored_snippet_path):
    logger.info(
        f"Replacing method in file: {path} at line: {line} "
        f"using refactored snippet: {refactored_snippet_path}"
    )

    try:
        result = subprocess.run(
            [
                'java', '-jar', 'tools/method-toolkit-1.0.jar',
                'replace',
                path,
                str(line),
                refactored_snippet_path
            ],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info("Method replacement completed successfully.")
        return result.stdout

    except subprocess.CalledProcessError as e:
        logger.error(
            f"Method replacement failed for {path} at line {line}: {e}. "
            f"STDERR: {e.stderr}"
        )
        raise

    except Exception as e:
        logger.error(
            f"Unexpected error during method replacement for {path}: {e}"
        )
        raise

def restore_original_class(path):
    logger.info(f"Restoring original class from backup: {path}")

    try:
        result = subprocess.run(
            ['java', '-jar', 'tools/method-toolkit-1.0.jar', 'restore', path],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info("Restore completed successfully.")
        return result.stdout

    except subprocess.CalledProcessError as e:
        logger.error(f"Restore failed for {path}: {e}. STDERR: {e.stderr}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error during restore for {path}: {e}")
        raise

def snippet_to_file(snippet, id):
    output_dir = "outputs/snippets"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"code_{id}.java")

    logger.info(f"Writing snippet to file: {file_path}")

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(snippet)
        logger.info(f"Snippet successfully written to {file_path}")
    except Exception as e:
        logger.error(f"Failed to write snippet to {file_path}: {e}")
        raise

def build_repository(repository_path):
    logger.info(f"Starting Maven build in: {repository_path}")

    result = subprocess.run(
        ['mvn', 'clean', 'install', '-Dcheckstyle.skip=true'],
        capture_output=True,
        text=True,
        shell=True,
        cwd=repository_path
    )

    if result.returncode == 0:
        logger.info("Build completed successfully.")
    else:
        logger.error(f"Build failed with return code {result.returncode}.")
        logger.error(f"STDERR: {result.stderr}")

    return result.stdout

def analyze_build_output(output):
    if "BUILD SUCCESS" in output:
        logger.info("Build result: SUCCESS")
        return "SUCCESS"
    elif "COMPILATION ERROR" in output:
        logger.warning("Build result: COMPILATION_ERROR")
        return "COMPILATION_ERROR"
    elif "There are test failures" in output or ("Tests run:" in output and "Failures:" in output):
        logger.warning("Build result: TEST_FAILURE")
        return "TEST_FAILURE"
    elif "BUILD FAILURE" in output:
        logger.warning("Build result: UNKNOWN_FAILURE")
        return "UNKNOWN_FAILURE"
    else:
        logger.warning("Build result: UNKNOWN")
        return "UNKNOWN"
