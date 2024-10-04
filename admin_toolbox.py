import os
import xml.etree.ElementTree as ET
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import time
import logging

# Configure logging
logging.basicConfig(filename='AdminToolbox.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_action(action, level=logging.INFO):
    # Log to GUI log file
    with open("gui_log.txt", "a") as log_file:
        log_file.write(f"{action}\n")
    
    # Log to AdminToolbox.log
    logging.log(level, action)

def get_registry_key_value(key, value_name):
    log_action(f"Registry key retrieval simulated for {key}\\{value_name}")
    return platform.version()

def compare_version(current_version, target_version):
    result = "Version matches" if current_version == target_version else "Version does not match"
    log_action(f"Version comparison: {result}")
    return f"{result}. Current: {current_version}, Target: {target_version}"

def read_xml_file(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        log_action(f"XML file read successfully: {file_path}")
        return "XML file read successfully.", ET.tostring(root, encoding='unicode')
    except FileNotFoundError:
        log_action(f"XML file not found: {file_path}", logging.ERROR)
        return f"The file '{file_path}' does not exist.", None
    except ET.ParseError:
        log_action(f"Failed to parse XML file: {file_path}", logging.ERROR)
        return f"Failed to parse the XML file: {file_path}", None

def simulate_admin_permissions(username, action):
    if action.lower() not in ['grant', 'revoke']:
        log_action(f"Invalid admin action: {action}", logging.ERROR)
        return "Invalid action. Use 'grant' or 'revoke'."

    result = f"Admin permissions {action.lower()}ed {'to' if action.lower() == 'grant' else 'from'} {username}"
    log_action(result)
    return result

def execute_simulated_program(program_name, args):
    result = f"Simulating execution of program: {program_name}\nWith arguments: {args}\nProgram executed successfully."
    log_action(result)
    return result

class AdminToolboxGUI:
    def __init__(self, master):
        self.master = master
        master.title("AdminToolbox")
        master.geometry("400x300")

        self.buttons = [
            ("Registry Key Retrieval", self.registry_key_retrieval),
            ("Compare Versions", self.compare_versions),
            ("Read XML File", self.read_xml),
            ("Admin Permissions", self.admin_permissions),
            ("Execute Program", self.execute_program)
        ]

        for text, command in self.buttons:
            tk.Button(master, text=text, command=command).pack(pady=5)

        log_action("AdminToolbox GUI initialized")

        # Start the simulation after a short delay
        self.master.after(1000, self.start_simulation)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)
        log_action(f"Message shown: {title} - {message}")

    def registry_key_retrieval(self):
        log_action("Registry Key Retrieval button clicked")
        key = "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"
        value_name = "ProductName"
        result = get_registry_key_value(key, value_name)
        self.show_message("Registry Key Retrieval", f"Retrieved value: {result}")

    def compare_versions(self):
        log_action("Compare Versions button clicked")
        current_version = "1.0.0"
        target_version = "1.1.0"
        result = compare_version(current_version, target_version)
        self.show_message("Version Comparison", result)

    def read_xml(self):
        log_action("Read XML File button clicked")
        file_path = "example.xml"
        message, content = read_xml_file(file_path)
        if content:
            self.show_message("XML File Contents", f"{message}\n\n{content}")
        else:
            self.show_message("XML File Error", message)

    def admin_permissions(self):
        log_action("Admin Permissions button clicked")
        username = "testuser"
        action = "grant"
        result = simulate_admin_permissions(username, action)
        self.show_message("Admin Permissions", result)

    def execute_program(self):
        log_action("Execute Program button clicked")
        program_name = "test_program.exe"
        args = "--verbose"
        result = execute_simulated_program(program_name, args)
        self.show_message("Program Execution", result)

    def start_simulation(self):
        for _, command in self.buttons:
            self.master.after(1000, command)
        self.master.after(6000, self.master.quit)

def main():
    log_action("AdminToolbox application started")
    root = tk.Tk()
    AdminToolboxGUI(root)
    root.mainloop()
    log_action("AdminToolbox application closed")

if __name__ == "__main__":
    main()
