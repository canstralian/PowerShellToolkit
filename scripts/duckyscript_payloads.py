import time
import pyautogui
import os
import json

class DuckyScriptPayload:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def execute(self):
        lines = self.content.split('\n')
        for line in lines:
            self._execute_command(line.strip())

    def _execute_command(self, command):
        parts = command.split(' ', 1)
        cmd = parts[0].upper()
        arg = parts[1] if len(parts) > 1 else ''

        if cmd == 'DELAY':
            time.sleep(float(arg) / 1000)
        elif cmd == 'STRING':
            pyautogui.typewrite(arg)
        elif cmd == 'GUI':
            pyautogui.hotkey('win', arg.lower())
        elif cmd == 'ENTER':
            pyautogui.press('enter')
        # Add more command implementations as needed

def load_duckyscript_payload(name, content):
    return DuckyScriptPayload(name, content)

def list_duckyscript_payloads():
    payloads_dir = 'duckyscript_payloads'
    if not os.path.exists(payloads_dir):
        os.makedirs(payloads_dir)
    
    payloads = []
    for filename in os.listdir(payloads_dir):
        if filename.endswith('.json'):
            with open(os.path.join(payloads_dir, filename), 'r') as f:
                payload = json.load(f)
                payloads.append(payload['name'])
    return payloads

def save_duckyscript_payload(name, content):
    payloads_dir = 'duckyscript_payloads'
    if not os.path.exists(payloads_dir):
        os.makedirs(payloads_dir)
    
    payload = {
        'name': name,
        'content': content
    }
    with open(os.path.join(payloads_dir, f"{name}.json"), 'w') as f:
        json.dump(payload, f)

def execute_duckyscript_payload(payload_name):
    payloads_dir = 'duckyscript_payloads'
    payload_path = os.path.join(payloads_dir, f"{payload_name}.json")
    
    if not os.path.exists(payload_path):
        return f"Payload '{payload_name}' not found"
    
    with open(payload_path, 'r') as f:
        payload_data = json.load(f)
        payload = DuckyScriptPayload(payload_data['name'], payload_data['content'])
        payload.execute()
    
    return f"Executed payload: {payload_name}"

# Additional function to get payload content
def get_duckyscript_payload_content(payload_name):
    payloads_dir = 'duckyscript_payloads'
    payload_path = os.path.join(payloads_dir, f"{payload_name}.json")
    
    if not os.path.exists(payload_path):
        return None
    
    with open(payload_path, 'r') as f:
        payload_data = json.load(f)
        return payload_data['content']
