import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
LLM_BASE_URL = os.getenv('LLM_BASE_URL')
LLM_MODEL = os.getenv('LLM_MODEL')

base = {
    'model': LLM_MODEL,
    'messages': [
        {'role': 'system', 'content': 'You are a personal finance coach.'},
        {'role': 'user', 'content': 'My monthly income is 60000 and I spend around 45000. Can you analyze my finances?'}
    ],
    'temperature': 0.7,
}

func = {
    'name': 'calculate_expenses',
    'description': 'Calculate total income, total expenses, monthly savings, savings rate, and budget gaps from provided income and expense values.',
    'parameters': {
        'type': 'object',
        'properties': {
            'income': {'type': 'number', 'description': 'Total monthly income.'},
            'expenses': {
                'type': 'object',
                'description': 'Monthly expenses grouped by category.',
                'additionalProperties': {'type': 'number'},
            },
        },
        'required': ['income', 'expenses'],
    },
}

test_payloads = [
    ('functions + function_call', {**base, 'functions': [func], 'function_call': 'auto'}),
    ('tools + tool_choice + type tool', {**base, 'tools': [{**func, 'type': 'tool'}], 'tool_choice': 'auto'}),
    ('tools + tool_choice + type function', {**base, 'tools': [{**func, 'type': 'function'}], 'tool_choice': 'auto'}),
    ('tools + tool_choice + function wrapper', {**base, 'tools': [{'type':'function', 'function': func}], 'tool_choice': 'auto'}),
    ('tools + tool_choice + function wrapper + name', {**base, 'tools': [{'type':'function', 'name': 'calculate_expenses', 'function': func}], 'tool_choice': 'auto'}),
    ('tools + tool_choice no type', {**base, 'tools': [func], 'tool_choice': 'auto'}),
    ('tools + tool_choice auto dict', {**base, 'tools': [{**func, 'type': 'function'}], 'tool_choice': {'name':'auto'}}),
    ('functions only', {**base, 'functions': [func]}),
]

headers = {
    'Authorization': f'Bearer {OPENROUTER_API_KEY}',
    'Content-Type': 'application/json',
}

for name, payload in test_payloads:
    print('TEST:', name)
    print('payload keys:', payload.keys())
    r = requests.post(LLM_BASE_URL, headers=headers, json=payload, timeout=20)
    print('STATUS:', r.status_code)
    print(r.text)
    print('-----\n')
