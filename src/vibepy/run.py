import code
from code import InteractiveInterpreter 
## using exec
import os
import itertools  # Import itertools for permutations
import logging
import subprocess
## compile the code

def run_python_code(codeblock):
    language = codeblock.language
    assert language in ["python", ""]
    source = codeblock.code
    logging.debug(f"Running Python code:\n{source}")
    compile_code = code.compile_command(source, '<string>', 'exec')
    logging.debug(f"Compiled code: {compile_code}")
    InteractiveInterpreter().runcode(compile_code)

def run_shell_code(codeblock):
    language = codeblock.language
    assert language == "bash"
    source = codeblock.code
    logging.debug(f"Running shell code:\n{source}")
    
    # Split the source into individual commands and handle paths
    commands = []
    for cmd in source.split('\n'):
        cmd = cmd.strip()
        if not cmd or cmd.startswith('#'):
            continue
        # Handle relative paths in commands
        if cmd.startswith('cd '):
            path = cmd[3:].strip()
            if not os.path.isabs(path):
                # Convert relative path to absolute path
                path = os.path.abspath(path)
            cmd = f'cd "{path}"'
        commands.append(cmd)
    
    logging.debug(f"Commands to run: {commands}")
    for cmd in commands:
        try:
            logging.debug(f"Running command: {cmd}")
            # Use subprocess to run each command
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running command '{cmd}': {e}")
            if e.stdout:
                print(e.stdout)
            if e.stderr:
                print(e.stderr)
            raise

def run_code_single(codeblock):
    language = codeblock.language
    logging.debug(f"Running code block with language: {language}")
    logging.debug(f"Code content:\n{codeblock.code}")
    if language in ["python", ""]:
        run_python_code(codeblock)
    elif language == "bash":
        run_shell_code(codeblock)

def run_code_ordered(codeblocks):
    for cb in codeblocks:
        logging.info(f"Running {cb.language} codeblock: {cb.code}")
        try:
            run_code_single(cb)
        except Exception as e:
            logging.error(f"Error running codeblock: {e}")
            raise

def run_code_permutations(codeblocks, retry_count=0, max_retries=3):
    # Generate all permutations of the codeblocks
    for perm in itertools.permutations(codeblocks):
        logging.info(f"Trying permutation: {[cb.language for cb in perm]}")
        try:
            run_code_ordered(perm)  # Run the code blocks in this permutation
            return  # If successful, exit
        except Exception as e:
            logging.error(f"Permutation failed: {e}")
            if retry_count < max_retries:
                retry_count += 1
            else:
                logging.error("Max retries reached. Stopping execution.")
                raise

