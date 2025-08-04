# Vibepy

Talking to and running codes from open-ai.

It has context memory for all conversations in one session before exit.

## Installation

```bash
pip install vibepy
```
Or if use uv  

```bash
uv  pip install --no-cache vibepy==0.2.4
```

## Usage

To use Vibepy, you need to set up your API key. The tool supports both OpenAI and OpenRouter.

### For OpenRouter Users (Recommended)

Set the following environment variables:

```bash
export OPENROUTER_API_KEY="YOUR_OPENROUTER_KEY"
export OPENROUTER_API_BASE="https://openrouter.ai/api/v1"
```

### For OpenAI Users

Set the following environment variable:

```bash
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

### Running Vibepy

1.  **Start the interactive REPL:**

    ```bash
    vibepy
    ```

2.  **Specify a model:**

    The default model is `gpt-4o-mini`. You can specify a different one using the `--model` flag.

    ```bash
    vibepy --model gpt-4-turbo
    ```

3.  **Execute code automatically:**

    Use the `-e` or `--execute` flag to automatically run the code blocks from the AI's response.

    ```bash
    vibepy -e
    ```

    If the code encounters an error, Vibepy will automatically retry up to 5 times, feeding the error back to the model for debugging. If it still fails, you can provide additional input to help the model fix the code.

## License

MIT License
