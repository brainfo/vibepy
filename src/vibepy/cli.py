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
    parser.add_argument("--api-key", type=str, default=os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY"), help="API key for the service")
    parser.add_argument("--base-url", type=str, default=os.environ.get("OPENROUTER_API_BASE") or os.environ.get("OPENAI_API_BASE"), help="Base URL for the API")
    return parser.parse_args()

def run_vibepy(execute: bool = False, model: str = "gpt-4o-mini", api_key: str = None, base_url: str = None):
    """Run vibepy.py with the specified run parameter."""
    vibepy_main(execute=execute, model=model, api_key=api_key, base_url=base_url)

def main():
    args = parse_args()
    run_vibepy(execute=args.execute, model=args.model, api_key=args.api_key, base_url=args.base_url)

if __name__ == "__main__":
    main() 