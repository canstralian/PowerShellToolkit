import os
import xml.etree.ElementTree as ET
import platform
import subprocess
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='AdminToolbox.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_action(action, level=logging.INFO):
    # Log to GUI log file
    with open("gui_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - {action}\n")
    
    # Log to AdminToolbox.log
    logging.log(level, action)

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log_action(f"Command failed: {e}", logging.ERROR)
        return f"Error: {e.stderr.strip()}"

def get_registry_key_value(key, value_name, computer_name=None):
    if platform.system() != "Windows":
        message = (
            "Registry operations are only supported on Windows systems. "
            "For non-Windows systems, consider using alternative methods:\n"
            "- Linux: Use the 'sysctl' command or read from /proc filesystem\n"
            "- macOS: Use the 'defaults' command\n"
            "For cross-platform compatibility, consider storing configuration "
            "in XML or JSON files instead of the registry."
        )
        log_action(f"Registry operation attempted on non-Windows system: {platform.system()}", logging.WARNING)
        return message
    
    if computer_name and computer_name.lower() != "localhost":
        command = f"reg query \\\\{computer_name}\\{key} /v {value_name}"
    else:
        command = f"reg query {key} /v {value_name}"
    
    result = run_command(command)
    log_action(f"Registry key retrieval for {key}\\{value_name}{' on ' + computer_name if computer_name else ''}")
    return result

def compare_version(current_version, target_version):
    result = "Version matches" if current_version == target_version else "Version does not match"
    log_action(f"Version comparison: {result}")
    return f"{result}. Current: {current_version}, Target: {target_version}"

def read_xml_file(file_path):
    try:
        # Get the absolute path
        abs_file_path = os.path.abspath(file_path)
        logging.debug(f"Attempting to read XML file from absolute path: {abs_file_path}")
        
        if not os.path.exists(abs_file_path):
            logging.error(f"File does not exist: {abs_file_path}")
            return f"Error: XML file not found: {abs_file_path}", None
        
        logging.debug(f"File exists. Current working directory: {os.getcwd()}")
        
        tree = ET.parse(abs_file_path)
        root = tree.getroot()
        content = ET.tostring(root, encoding='unicode')
        log_action(f"XML file read successfully: {abs_file_path}")
        return "XML file read successfully.", content
    except FileNotFoundError:
        log_action(f"XML file not found: {abs_file_path}", logging.ERROR)
        return f"Error: XML file not found: {abs_file_path}", None
    except ET.ParseError as e:
        log_action(f"Failed to parse XML file: {abs_file_path}", logging.ERROR)
        return f"Error parsing XML file: {str(e)}", None
    except Exception as e:
        log_action(f"Failed to read XML file: {abs_file_path}", logging.ERROR)
        return f"Error reading XML file: {str(e)}", None

def write_xml_file(file_path, xml_content):
    try:
        root = ET.fromstring(xml_content)
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        log_action(f"XML file written: {file_path}")
        return "XML file written successfully."
    except ET.ParseError as e:
        log_action(f"Failed to parse XML content", logging.ERROR)
        return f"Error parsing XML content: {str(e)}"
    except Exception as e:
        log_action(f"Failed to write XML file: {file_path}", logging.ERROR)
        return f"Error writing XML file: {str(e)}"

def modify_xml_file(file_path, xpath, new_value):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for elem in root.findall(xpath):
            elem.text = new_value
            log_action(f"XML file modified: {file_path}")
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
            return "XML file modified successfully."
        return "XPath not found in the XML file."
    except FileNotFoundError:
        log_action(f"XML file not found: {file_path}", logging.ERROR)
        return f"Error: XML file not found: {file_path}"
    except ET.ParseError as e:
        log_action(f"Failed to parse XML file: {file_path}", logging.ERROR)
        return f"Error parsing XML file: {str(e)}"
    except Exception as e:
        log_action(f"Failed to modify XML file: {file_path}", logging.ERROR)
        return f"Error modifying XML file: {str(e)}"

def manage_admin_permissions(username, action):
    if platform.system() != "Windows":
        return "Admin permissions management is only supported on Windows systems."
    
    command = f"net {action.lower()} Administrators {username}"
    result = run_command(command)
    log_action(f"Admin permissions {action.lower()}ed for {username}")
    return result

def execute_program(program_name, args):
    command = f"{program_name} {args}"
    result = run_command(command)
    log_action(f"Executed program {program_name}")
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/is_windows', methods=['GET'])
def is_windows():
    return jsonify({"is_windows": platform.system() == "Windows"})

@app.route('/api/registry_key', methods=['POST'])
def api_registry_key():
    data = request.json
    result = get_registry_key_value(data['key'], data['value_name'], data['computer_name'])
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
    app.run(host='0.0.0.0', port=5000, debug=True)
