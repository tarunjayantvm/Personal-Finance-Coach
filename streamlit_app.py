import json
import os
from typing import Any, Dict, List

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

if not OPENROUTER_API_KEY or not LLM_BASE_URL or not LLM_MODEL:
    st.warning("Please configure .env with OPENROUTER_API_KEY, LLM_BASE_URL, and LLM_MODEL.")

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

def call_llm(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "temperature": 0.7,
    }

    response = requests.post(LLM_BASE_URL, headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def extract_chat_content(response: Dict[str, Any]) -> str:
    if "choices" not in response or not response["choices"]:
        return "No response received from the LLM."

    choice = response["choices"][0]
    message = choice.get("message", {})
    return message.get("content", "No text content returned.")


def main() -> None:
    st.set_page_config(page_title="Personal Finance Coach", layout="wide")
    st.title("Personal Finance Coach")
    st.write("Chat with your finance coach and ask anything about budgeting, saving, expenses, or financial concepts.")

    st.subheader("Chat with your finance coach")
    user_question = st.text_area("Ask anything about budgeting, saving, or financial concepts", height=180)

    if st.button("Send Chat Message") and user_question.strip():
        messages = [
            {"role": "system", "content": "You are a personal finance coach."},
            {"role": "user", "content": user_question},
        ]
        try:
            response = call_llm(messages)
            assistant_text = extract_chat_content(response)
            st.markdown("### Coach Response")
            st.write(assistant_text)
        except Exception as exc:
            st.error(f"LLM request failed: {exc}")

    st.markdown("---")
    st.caption("Powered by Streamlit and OpenRouter-compatible LLM calls.")


if __name__ == "__main__":
    main()
