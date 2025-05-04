# Vibepy

Talking to and running codes from open-ai.

- [ ] I yoloed with agent and it now doesn't have the feature to keep contexts (more than one conversations). fixing

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
vibepy --model gpt-4.1
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

Cases when running `vibepy -e`

```bash
Welcome to Vibepy!  
Press 'q' to exit  
Say something: I have a pyproject.toml, please add a [build-system] section and add torch in it  

Vibepy: ```python
# Add torch to the build-system in pyproject.toml using uv.  

source .venv/bin/activate  
uv add --dev build  
uv pip install torch  
```  

```python  
# Python snippet to modify pyproject.toml  

import tomllib  
import tomli_w  

with open("pyproject.toml", "rb") as f:  
    data = tomllib.load(f)  

# Add build-system section if missing  
if "build-system" not in data:  
    data["build-system"] = {}  

# These values are standard PEP 517/518 defaults, but we include torch as requested.  
data["build-system"]["requires"] = ["setuptools>=42", "wheel", "torch"]  
data["build-system"]["build-backend"] = "setuptools.build_meta"  

with open("pyproject.toml", "wb") as f:  
   tomli_w.dump(data, f)  
```  
This will:  
- Activate the environment  
- Install build tools and torch  
- Patch your TOML to have a proper `[build-system]` section with `torch` as a build-time requirement.  

ERROR:root:Error running codeblock: invalid syntax (<string>, line 5). 
Attempt 1/5 failed: invalid syntax (<string>, line 5)  
Retrying with error feedback...  

Vibepy: ```bash  
source .venv/bin/activate 
uv add --dev build  
uv pip install torch  
uv pip install tomli tomli-w  
```

```python  
import tomli  
import tomli_w  

# Read the existing pyproject.toml  
with open("pyproject.toml", "rb") as f:  
    data = tomli.load(f)  

# Add or update the build-system section  
data["build-system"] = {  
    "requires": ["setuptools>=42", "wheel", "torch"],  
    "build-backend": "setuptools.build_meta"  
}  

# Write back the modified pyproject.toml  
with open("pyproject.toml", "wb") as f:  
    tomli_w.dump(data, f)  
```  
This script will:  
- Install any required tools.  
- Read and update your `pyproject.toml` validly.  

ERROR:root:Error running command 'uv add --dev build': Command 'uv add --dev build' returned non-zero exit status 2.  
error: No `project` table found in: `/mnt/run/jh/projects/pcos_sp/pyproject.toml`  

ERROR:root:Error running codeblock: Command 'uv add --dev build' returned non-zero exit status 2.  
Attempt 2/5 failed: Command 'uv add --dev build' returned non-zero exit status 2.  
Retrying with error feedback...  

Vibepy: ```bash  
source .venv/bin/activate  
uv pip install torch tomli tomli-w  
```  

```python 
import tomli  
import tomli_w  

with open("pyproject.toml", "rb") as f:  
    data = tomli.load(f)  

data["build-system"] = {  
    "requires": ["setuptools>=42", "wheel", "torch"],  
    "build-backend": "setuptools.build_meta"  
}  

with open("pyproject.toml", "wb") as f:  
    tomli_w.dump(data, f)  
```  

Say something: q  

Vibepy: It seems like your message got cut off. Could you please provide more details or clarify your request?


Exiting vibepy...  
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"
```

## License

MIT License
