import requests, os
from dotenv import load_dotenv
load_dotenv()
COORD = os.getenv('COORD_URL', 'http://localhost:8000')

def start_and_chat():
    r = requests.post(f'{COORD}/start_convo')
    body = r.json()
    sid = body['session_id']
    print('Agent:', body['prompt'])
    while True:
        text = input('You: ')
        if text.lower() in ('quit','exit'):
            break
        r = requests.post(f'{COORD}/reply', json={'session_id': sid, 'text': text})
        data = r.json()
        if 'plan' in data:
            print('\\n=== Trip Plan ===\\n')
            print(data['plan'])
            print('\\n=== End ===\\n')
        else:
            print('Agent:', data.get('prompt') or data)
    print('Goodbye.')

if __name__ == '__main__':
    start_and_chat()
