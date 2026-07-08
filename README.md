# Personal Finance Coach

A Streamlit app that analyzes monthly income and expenses, recommends budgeting and saving strategies, and provides a finance coaching chat experience using an OpenRouter-compatible LLM.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file from `.env.example` and add your OpenRouter API key.

3. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Environment variables

- `OPENROUTER_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL`


