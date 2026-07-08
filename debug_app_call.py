from streamlit_app import call_llm, CALCULATOR_TOOL
import json

messages = [
    {'role': 'system', 'content': 'You are a personal finance coach.'},
    {'role': 'user', 'content': 'My monthly income is 60000 and I spend around 45000. Can you analyze my finances?'}
]

response = call_llm(messages, tools=[CALCULATOR_TOOL])
print(json.dumps(response, indent=2)[:2000])
