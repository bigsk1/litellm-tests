# LiteLLM Test Scripts Setup Instructions

This document provides instructions for setting up and running the LiteLLM test scripts.

## Prerequisites

- Python 3.7 or later
- pip (Python package manager)

## Setup Steps

1. **Create a project directory**
   ```bash
   mkdir litellm-tests
   cd litellm-tests
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install litellm python-dotenv
   ```

4. **Create a `.env` file**
   
   Create a file named `.env` in your project directory and add your API keys, add keys and model providers as needed:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   # GOOGLE_API_KEY=your_google_api_key
   ```

5. **Create a directory for test files**
   ```bash
   mkdir docs
   ```

6. **Add test files (optional)**
   - For long context tests: Add a long text file (e.g., a transcript) in the `docs` folder
   - For image tests: Add an image file (e.g., a JPEG) in the `docs` folder

## Running the Test Scripts

Place each of the test scripts in your project directory and run them individually:

```bash
python basic-completion.py
python system-message-test.py
python long-context-test.py
python streaming-test.py
python tool-calling-test.py
python image-input-test.py
```

## Modifying the Scripts

- To test different models, update the `models` list in each script
- Adjust the parameters (e.g., temperature, max_tokens) according to your requirements
- For the long context test, update the file path in the script to your text file

## Troubleshooting

- If you encounter API key errors, check that your `.env` file is correctly formatted and the keys are valid
- For context length errors, try using a smaller text file or a model with a larger context window
- For image input errors, ensure your image file exists and is in a supported format (JPEG, PNG)

## Additional Features to Test

The scripts cover the main features mentioned in the transcript:
- Basic completion
- System messages
- Long context
- Streaming
- Tool calling
- Image input

If you want to test additional features:
- Modify parameters (temperature, top_p, etc.)
- Test with different prompts
- Try different model versions
