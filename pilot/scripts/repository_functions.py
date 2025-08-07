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

def commit_repository(repo_path, sample_id):
    try:
        repo_path = os.path.abspath(repo_path)
        logger.info("Staging all changes in repository: %s", repo_path)

        subprocess.run(['git', 'add', '.'], check=True, cwd=repo_path)
        
        staged = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            check=True, cwd=repo_path,
            capture_output=True, text=True
        ).stdout.strip()

        if not staged:
            logger.info("No changes to commit.")
            return False

        commit_msg = f"Refactored method {sample_id} for analysis"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True, cwd=repo_path)
        logger.info("Committed change: %s", commit_msg)
        return True

    except subprocess.CalledProcessError as e:
        logger.error("Git command failed (returncode=%s): %s", e.returncode, e.stderr)
    except Exception as e:
        logger.error("Error committing change: %s", e)

    return False

def rollback_commit(repo_path):
    try:
        subprocess.run(['git', 'reset', '--hard', 'original'], check=True, cwd=repo_path)
        logger.info("Repository rolled back to previous commit.")
    except Exception as e:
        logger.error(f"Error rolling back commit: {e}")