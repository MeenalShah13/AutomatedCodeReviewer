# Automated Code Reviewer

This automated code reviewer was made to simplify reviewing open-source code and to allow one to get code reviewed independently.

## Usage

### Note
- To get started, ensure Python version 3.10 or higher is installed on your laptop.
- This script is developed for Windows 11 system and may break on another OS.

### Installation
1. Install Ollama for Windows from [ollama.com](https://ollama.com).

2. Open Command Prompt on your device. Run the following commands one by one.
    ```bash
    ollama pull gemma3:4b
    ollama serve
    ```
    *Note:* The last command may end up in an error saying the port is already taken. If so, then ollama is already running on your system.

3. Create a virtual environment in the folder where this script is present:
    ```bash
    python -m venv <virtual_env_name>
    ```

4. Activate the virtual environment from the root of the folder:
    ```bash
    <virtual_env_name>/Scripts/activate
    ```

5. Run the following command to install all required dependencies:
    ```bash
    python -r requirements.txt
    ```  

6. Run [codeReview.py](codeReview.py)

The program will prompt you to enter the patch URL for which you want to review.  
Enter the URL in the format `http://{base-url}/c/{patch-id}` (Example: https://gerrit.cloudera.org/c/22914/).

## Tech Stack
This project uses [Ollama](https://ollama.com) to handle installation, hosting and usage of LLM Models. It uses [gemma3:4b](https://ollama.com/library/gemma3:4b) model to provide suggestions.  
This project also makes use of [Gerrit API](https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html) to fetch relevant information of the patch, the files changes, reviewer comments as well as file difference.

## Future Work
1. Using a better LLM model, that is fast, as well as accurate to provide better suggestions.
2. Using context history of the patch, after comparison with the older revisions and/or patches to provide better suggestions.
3. Improve prompt engineering for the LLM model, to optionally accept context input from the user, as well as to provide better suggestions.
4. Create a workflow such that the user, after giving their credentials can optionally post the comments directly to patch, after explicit permission to do so.