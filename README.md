# Vibepy

Talking to and running codes from open-ai.

## Installation

```bash
pip install vibepy
```
Or if use uv  

```bash
uv  pip install --no-cache vibepy==0.2.3
```

## Usage

Have OPENAI_API_KEYS as one of your environment variables.  

1. Start the vibepy CLI, and have conversation with open-ai

    Default gpt-4o-mini

```bash
vibepy
```
2. Specify model

```bash
vibepy --model gpt-4.1-mini
```

3. automatically run the returned code blocks:  

```bash
vibepy -e
```

This will automatically run the returned code blocks once and present again a user input prompt.  
If the execution returns errors,  
You can then either 
    - press any key, or add say anything (add information) to continue, then it will catch the error messages and input to the model to debug until 5 times
    - press q to quit

## License

MIT License
