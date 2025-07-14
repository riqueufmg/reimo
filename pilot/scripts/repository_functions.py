import pandas as pd
import subprocess
import time
import os
import logging

logger = logging.getLogger(__name__)

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

def commit_repository(modified_file, sample_id):
    try:
        logger.info(f"Staging file for commit: {modified_file}")

        subprocess.run(['git', 'add', modified_file], check=True)
        commit_msg = f"Refactored method {sample_id} for analysis"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)

        logger.info(f"Committed change: {commit_msg}")
    except Exception as e:
        logger.error(f"Error commit change: {e}")

def rollback_commit(sample_id):
    try:
        subprocess.run(['git', 'reset', '--hard', 'HEAD~1'], check=True)
        logger.info("Repository rolled back to previous commit.")
    except Exception as e:
        logger.error(f"Error roolback commit: {e}")