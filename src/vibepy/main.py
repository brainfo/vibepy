"""
Vibepy: A Python REPL talking to and running codes from open-ai
"""

import argparse
import sys
import os
import time
from pathlib import Path
from colorama import init, Fore
from openai import OpenAI
import requests
from vibepy import codeblock, run


def run_universal_mode(execute: bool = False, model: str = "gpt-4o-mini", api_key: str = None, base_url: str = None):
    init()  # Initialize colorama

    client = OpenAI(api_key=api_key, base_url=base_url)

    print(Fore.GREEN + "Welcome to Vibepy!")
    print(Fore.YELLOW + "Press 'q' to exit")
    role_spec = "You are a helpful Python coding assistant. Please first use uv to manage the environment: source .venv/bin/activate, then using uv add or uv pip install, then generate the code to be executed. Please keep the code blocks as few as possible and in order of being executed. formatting is critical, including indentations and special characters."
    
    # Initialize conversation history with system message
    messages = [{"role": "system", "content": role_spec}]

    while True:
        user_input = input(Fore.CYAN + "Say something: ")

        if user_input.startswith('@'):
            file_path = Path(user_input[1:])
            if file_path.exists():
                user_input = file_path.read_text()
            else:
                print(Fore.RED + f"File not found: {file_path}")
                continue

        try:
            # Add user message to history
            messages.append({"role": "user", "content": user_input})
            
            # Get OpenAI's response
            response = client.chat.completions.create(model=model,
            messages=messages)
            reply = response.choices[0].message.content
            
            # Add assistant's response to history
            messages.append({"role": "assistant", "content": reply})
            
            print(Fore.RED + "\nVibepy: " + reply + "\n")
            
            if execute:
                # Create code blocks from the reply
                code_blocks = codeblock.create_code_block(reply)
                max_retries = 5
                retry_count = 0
                last_error = None
                
                while retry_count < max_retries:
                    try:
                        # Try running the code blocks in order
                        run.run_code_ordered(code_blocks)
                        break  # Success, exit retry loop
                    except Exception as e:
                        last_error = str(e)
                        retry_count += 1
                        if retry_count < max_retries:
                            print(Fore.YELLOW + f"Attempt {retry_count}/{max_retries} failed: {last_error}")
                            print(Fore.YELLOW + "Retrying with error feedback...")
                            
                            # Add error feedback to messages
                            error_message = f"The code failed with error: {last_error}. Please fix the code and try again."
                            messages.append({"role": "user", "content": error_message})
                            
                            # Get new response with error feedback
                            error_response = client.chat.completions.create(
                                model=model,
                                messages=messages
                            )
                            reply = error_response.choices[0].message.content
                            messages.append({"role": "assistant", "content": reply})
                            print(Fore.RED + "\nVibepy: " + reply + "\n")
                            code_blocks = codeblock.create_code_block(reply)
                        else:
                            print(Fore.RED + f"Failed after {max_retries} attempts. Last error: {last_error}")
                            # If all retries fail, try all permutations as last resort
                            try:
                                run.run_code_permutations(code_blocks)
                            except Exception as e:
                                print(Fore.RED + f"All execution attempts failed: {str(e)}")
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")

        if user_input == 'q':
            print(Fore.RED + "\nExiting vibepy...")
            break

        print(Fore.YELLOW + "Press 'q' to exit")

import time


def run_openai_assistant_mode(execute: bool = False, model: str = "gpt-4o-mini", api_key: str = None, base_url: str = None):
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # Create an assistant
    assistant = client.beta.assistants.create(
        name="Vibepy Assistant",
        instructions="You are a helpful Python coding assistant. Please first use uv to manage the environment: source .venv/bin/activate, then using uv add or uv pip install, then generate the code to be executed. Please keep the code blocks as few as possible and in order of being executed. formatting is critical, including indentations and special characters.",
        tools=[{"type": "code_interpreter"}],
        model=model,
    )

    # Create a thread
    thread = client.beta.threads.create()

    print(Fore.GREEN + "Welcome to Vibepy (OpenAI Assistant Mode)!")
    print(Fore.YELLOW + "Press 'q' to exit")

    while True:
        user_input = input(Fore.CYAN + "Say something: ")

        if user_input.lower() == 'q':
            print(Fore.RED + "\nExiting vibepy...")
            break

        if user_input.startswith('@'):
            file_path = Path(user_input[1:])
            if file_path.exists():
                user_input = file_path.read_text()
            else:
                print(Fore.RED + f"File not found: {file_path}")
                continue
        
        # Add user message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        # Run the assistant
        run_instance = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        # Wait for the run to complete
        while run_instance.status != "completed":
            run_instance = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run_instance.id)
            if run_instance.status == "failed":
                print(Fore.RED + "Run failed: " + run_instance.last_error.message)
                break
            time.sleep(1)

        # Retrieve and display messages
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        for msg in reversed(messages.data):
            if msg.role == "assistant":
                reply = msg.content[0].text.value
                print(Fore.RED + "\nVibepy: " + reply + "\n")
                if execute:
                    code_blocks = codeblock.create_code_block(reply)
                    try:
                        run.run_code_ordered(code_blocks)
                    except Exception as e:
                        print(Fore.RED + f"Execution failed: {e}")

        print(Fore.YELLOW + "Press 'q' to exit")

def main(execute: bool = False, model: str = "gpt-4o-mini", api_key: str = None, base_url: str = None, agent: str = "universal"):
    if agent == "universal":
        run_universal_mode(execute=execute, model=model, api_key=api_key, base_url=base_url)
    elif agent == "openai":
        run_openai_assistant_mode(execute=execute, model=model, api_key=api_key, base_url=base_url)
    else:
        print(Fore.RED + f"Unknown agent: {agent}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vibepy: talking to and running codes from open-ai")
    parser.add_argument("-e", "--execute", action="store_true", help="Execute code from responses")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model to use")
    parser.add_argument("--agent", type=str, default="universal", choices=["universal", "openai"], help="Agent to use")
    parser.add_argument("--api-key", type=str, help="API key for the service")
    parser.add_argument("--base-url", type=str, help="Base URL for the API")
    parser.add_argument("--openai", action="store_true", help="Force use of OpenAI API for universal agent")
    args = parser.parse_args()

    api_key = args.api_key
    base_url = args.base_url

    if args.agent == "openai" or args.openai:
        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY")
        if base_url is None and not args.openai: # only use base_url for non-default openai agent
            base_url = os.environ.get("OPENAI_API_BASE")
    else:  # universal without --openai
        if api_key is None:
            api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if base_url is None:
            base_url = os.environ.get("OPENROUTER_API_BASE") or os.environ.get("OPENAI_API_BASE")

    main(
        execute=args.execute,
        model=args.model,
        api_key=api_key,
        base_url=base_url,
        agent=args.agent
    )
