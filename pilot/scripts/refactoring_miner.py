import subprocess
import time
import os
import logging

logger = logging.getLogger(__name__)

def run_refactoringminer(repo_path, jar_path):
    try:
        #repo_abs_path = os.path.abspath(repo_path)
        repo_abs_path = os.path.abspath(repo_path).replace("\\", "/")
        
        start_commit = subprocess.run(
            ['git', 'rev-parse', 'original'],
            check=True,
            cwd=repo_path,
            capture_output=True,
            text=True
        ).stdout.strip()

        end_commit = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            check=True,
            cwd=repo_path,
            capture_output=True,
            text=True
        ).stdout.strip()

        logger.info("Comparing original (%s) -> current HEAD (%s)", start_commit, end_commit)

        cmd = [
            'java',
            '-Dorg.slf4j.simpleLogger.defaultLogLevel=error',
            '-Dorg.slf4j.simpleLogger.log.org.refactoringminer=error',
            '-jar', jar_path,
            '--mode=list',
            f'--start={start_commit}',
            f'--end={end_commit}',
            f'--repo={repo_abs_path}'
        ]

        result = subprocess.run(
            cmd,
            check=True,
            #cwd=repo_path,
            capture_output=True,
            text=True
        )
        logger.info("RefactoringMiner executed successfully.")
        logger.info("RefactoringMiner stdout:\n%s", result.stdout)
        return result.stdout

    except subprocess.CalledProcessError as e:
        logger.error("Command failed (returncode=%s): %s", getattr(e, 'returncode', 'N/A'), e.stderr)
    except Exception as e:
        logger.error("Error executing RefactoringMiner: %s", e)

    return None