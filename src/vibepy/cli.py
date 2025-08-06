"""
Vibepy CLI interface
"""

import argparse
import os
from .main import main as vibepy_main

def parse_args():
    parser = argparse.ArgumentParser(description="Vibepy: A Python REPL with hotkey functionality")
    parser.add_argument("-e", "--execute", action="store_true", help="Execute code from responses")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model to use")
    parser.add_argument("--api-key", type=str, help="API key for the service")
    parser.add_argument("--base-url", type=str, help="Base URL for the API")
    parser.add_argument("--agent", type=str, default="universal", choices=["universal", "openai"], help="Agent to use")
    parser.add_argument("--openai", action="store_true", help="Force use of OpenAI API for universal agent")
    return parser.parse_args()

def run_vibepy(execute: bool = False, model: str = "gpt-4o-mini", api_key: str = None, base_url: str = None, agent: str = "universal"):
    """Run vibepy.py with the specified run parameter."""
    vibepy_main(execute=execute, model=model, api_key=api_key, base_url=base_url, agent=agent)

def main():
    args = parse_args()
    
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

    run_vibepy(execute=args.execute, model=args.model, api_key=api_key, base_url=base_url, agent=args.agent)

if __name__ == "__main__":
    main() 