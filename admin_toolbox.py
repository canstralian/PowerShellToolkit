import os
import xml.etree.ElementTree as ET
import platform
import subprocess
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='AdminToolbox.log', level=logging.INFO, 
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
        return "Registry operations are only supported on Windows systems."
    
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
        tree = ET.parse(file_path)
        root = tree.getroot()
        content = ET.tostring(root, encoding='unicode')
        log_action(f"XML file read successfully: {file_path}")
        return "XML file read successfully.", content
    except FileNotFoundError:
        log_action(f"XML file not found: {file_path}", logging.ERROR)
        return f"Error: XML file not found: {file_path}", None
    except ET.ParseError as e:
        log_action(f"Failed to parse XML file: {file_path}", logging.ERROR)
        return f"Error parsing XML file: {str(e)}", None
    except Exception as e:
        log_action(f"Failed to read XML file: {file_path}", logging.ERROR)
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

def main():
    log_action("AdminToolbox application started")
    while True:
        print("\nAdminToolbox Menu:")
        print("1. Get Registry Key Value")
        print("2. Compare Versions")
        print("3. Read XML File")
        print("4. Write XML File")
        print("5. Modify XML File")
        print("6. Manage Admin Permissions")
        print("7. Execute Program")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            key = input("Enter registry key: ")
            value_name = input("Enter value name: ")
            result = get_registry_key_value(key, value_name)
        elif choice == '2':
            current_version = input("Enter current version: ")
            target_version = input("Enter target version: ")
            result = compare_version(current_version, target_version)
        elif choice == '3':
            file_path = input("Enter XML file path: ")
            result, content = read_xml_file(file_path)
            if content:
                print(content)
        elif choice == '4':
            file_path = input("Enter XML file path: ")
            xml_content = input("Enter XML content: ")
            result = write_xml_file(file_path, xml_content)
        elif choice == '5':
            file_path = input("Enter XML file path: ")
            xpath = input("Enter XPath: ")
            new_value = input("Enter new value: ")
            result = modify_xml_file(file_path, xpath, new_value)
        elif choice == '6':
            username = input("Enter username: ")
            action = input("Enter action (add/remove): ")
            result = manage_admin_permissions(username, action)
        elif choice == '7':
            program_name = input("Enter program name: ")
            args = input("Enter arguments: ")
            result = execute_program(program_name, args)
        elif choice == '8':
            log_action("AdminToolbox application exited")
            print("Exiting AdminToolbox. Goodbye!")
            break
        else:
            result = "Invalid choice. Please try again."
        
        print(f"\nResult: {result}")

if __name__ == '__main__':
    main()
