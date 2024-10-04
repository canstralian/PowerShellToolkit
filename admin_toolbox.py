import os
import xml.etree.ElementTree as ET
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
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

def run_powershell_command(command):
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log_action(f"PowerShell command failed: {e}", logging.ERROR)
        return f"Error: {e.stderr.strip()}"

def get_registry_key_value(key, value_name, computer_name=None):
    if computer_name:
        command = f"Invoke-Command -ComputerName {computer_name} -ScriptBlock {{ Get-ItemProperty -Path 'Registry::{key}' -Name {value_name} }}"
    else:
        command = f"Get-ItemProperty -Path 'Registry::{key}' -Name {value_name}"
    
    result = run_powershell_command(command)
    log_action(f"Registry key retrieval {'simulated ' if not computer_name else ''}for {key}\\{value_name}{' on ' + computer_name if computer_name else ''}")
    return result

def compare_version(current_version, target_version, computer_name=None):
    if computer_name:
        command = f"Invoke-Command -ComputerName {computer_name} -ScriptBlock {{ '{current_version}' -eq '{target_version}' }}"
    else:
        command = f"'{current_version}' -eq '{target_version}'"
    
    result = run_powershell_command(command)
    match_result = "Version matches" if result.lower() == "true" else "Version does not match"
    log_action(f"Version comparison on {computer_name or 'local'}: {match_result}")
    return f"{match_result}. Current: {current_version}, Target: {target_version}"

def read_xml_file(file_path, computer_name=None):
    if computer_name:
        command = f"Invoke-Command -ComputerName {computer_name} -ScriptBlock {{ [xml](Get-Content -Path '{file_path}') }}"
    else:
        command = f"[xml](Get-Content -Path '{file_path}')"
    
    try:
        result = run_powershell_command(command)
        log_action(f"XML file read successfully: {file_path}{' on ' + computer_name if computer_name else ''}")
        return "XML file read successfully.", result
    except Exception as e:
        log_action(f"Failed to read XML file: {file_path}{' on ' + computer_name if computer_name else ''}", logging.ERROR)
        return f"Error reading XML file: {str(e)}", None

def write_xml_file(file_path, xml_content, computer_name=None):
    if computer_name:
        command = f"Invoke-Command -ComputerName {computer_name} -ScriptBlock {{ $xml = [xml]'{xml_content}'; $xml.Save('{file_path}') }}"
    else:
        command = f"$xml = [xml]'{xml_content}'; $xml.Save('{file_path}')"
    
    result = run_powershell_command(command)
    log_action(f"XML file written: {file_path}{' on ' + computer_name if computer_name else ''}")
    return result

def modify_xml_file(file_path, xpath, new_value, computer_name=None):
    if computer_name:
        command = f"Invoke-Command -ComputerName {computer_name} -ScriptBlock {{ $xml = [xml](Get-Content -Path '{file_path}'); $node = $xml.SelectSingleNode('{xpath}'); if ($node) {{ $node.InnerText = '{new_value}'; $xml.Save('{file_path}'); 'XML file modified successfully.' }} else {{ 'XPath not found in the XML file.' }} }}"
    else:
        command = f"$xml = [xml](Get-Content -Path '{file_path}'); $node = $xml.SelectSingleNode('{xpath}'); if ($node) {{ $node.InnerText = '{new_value}'; $xml.Save('{file_path}'); 'XML file modified successfully.' }} else {{ 'XPath not found in the XML file.' }}"
    
    result = run_powershell_command(command)
    log_action(f"XML file modified: {file_path}{' on ' + computer_name if computer_name else ''}")
    return result

def manage_remote_admin_permissions(username, action, computer_name):
    command = f"Manage-RemoteAdminPermissions -Username {username} -Action {action} -ComputerName {computer_name}"
    result = run_powershell_command(command)
    log_action(f"Admin permissions {action.lower()}ed for {username} on {computer_name}")
    return result

def execute_remote_program(program_name, args, computer_name):
    command = f"Execute-RemoteProgram -ProgramPath '{program_name}' -Arguments '{args}' -ComputerName {computer_name}"
    result = run_powershell_command(command)
    log_action(f"Executed program {program_name} on {computer_name}")
    return result

class AdminToolboxGUI:
    def __init__(self, master):
        self.master = master
        master.title("AdminToolbox")
        master.geometry("500x500")

        self.computer_name = tk.StringVar(value="localhost")
        tk.Label(master, text="Computer Name:").pack(pady=5)
        tk.Entry(master, textvariable=self.computer_name).pack(pady=5)

        self.buttons = [
            ("Registry Key Retrieval", self.registry_key_retrieval),
            ("Compare Versions", self.compare_versions),
            ("Read XML File", self.read_xml),
            ("Write XML File", self.write_xml),
            ("Modify XML File", self.modify_xml),
            ("Admin Permissions", self.admin_permissions),
            ("Execute Program", self.execute_program)
        ]

        for text, command in self.buttons:
            tk.Button(master, text=text, command=command).pack(pady=5)

        log_action("AdminToolbox GUI initialized")
        
        # Display initial state
        self.show_initial_state()

    def show_initial_state(self):
        initial_state = f"AdminToolbox GUI initialized\n"
        initial_state += f"Remote computer management options available\n"
        initial_state += f"Current computer name: {self.computer_name.get()}\n"
        initial_state += f"Available functions: Registry Key Retrieval, Compare Versions, Read XML File, Write XML File, Modify XML File, Admin Permissions, Execute Program"
        print(initial_state)  # Print to console for shell feedback
        messagebox.showinfo("AdminToolbox Initial State", initial_state)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)
        log_action(f"Message shown: {title} - {message}")

    def registry_key_retrieval(self):
        log_action("Registry Key Retrieval button clicked")
        key = "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"
        value_name = "ProductName"
        result = get_registry_key_value(key, value_name, self.computer_name.get())
        self.show_message("Registry Key Retrieval", f"Retrieved value: {result}")

    def compare_versions(self):
        log_action("Compare Versions button clicked")
        current_version = simpledialog.askstring("Input", "Enter current version:")
        target_version = simpledialog.askstring("Input", "Enter target version:")
        result = compare_version(current_version, target_version, self.computer_name.get())
        self.show_message("Version Comparison", result)

    def read_xml(self):
        log_action("Read XML File button clicked")
        file_path = simpledialog.askstring("Input", "Enter XML file path:")
        message, content = read_xml_file(file_path, self.computer_name.get())
        if content:
            self.show_message("XML File Contents", f"{message}\n\n{content}")
        else:
            self.show_message("XML File Error", message)

    def write_xml(self):
        log_action("Write XML File button clicked")
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if file_path:
            xml_content = simpledialog.askstring("Input", "Enter XML content:")
            if xml_content:
                result = write_xml_file(file_path, xml_content, self.computer_name.get())
                self.show_message("Write XML File", result)
            else:
                self.show_message("Write XML File", "XML content is empty. Operation cancelled.")
        else:
            self.show_message("Write XML File", "No file selected. Operation cancelled.")

    def modify_xml(self):
        log_action("Modify XML File button clicked")
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            xpath = simpledialog.askstring("Input", "Enter XPath to modify:")
            new_value = simpledialog.askstring("Input", "Enter new value:")
            if xpath and new_value:
                result = modify_xml_file(file_path, xpath, new_value, self.computer_name.get())
                self.show_message("Modify XML File", result)
            else:
                self.show_message("Modify XML File", "XPath or new value is empty. Operation cancelled.")
        else:
            self.show_message("Modify XML File", "No file selected. Operation cancelled.")

    def admin_permissions(self):
        log_action("Admin Permissions button clicked")
        username = simpledialog.askstring("Input", "Enter username:")
        action = simpledialog.askstring("Input", "Enter action (Grant/Revoke):")
        result = manage_remote_admin_permissions(username, action, self.computer_name.get())
        self.show_message("Admin Permissions", result)

    def execute_program(self):
        log_action("Execute Program button clicked")
        program_name = simpledialog.askstring("Input", "Enter program path:")
        args = simpledialog.askstring("Input", "Enter program arguments:")
        result = execute_remote_program(program_name, args, self.computer_name.get())
        self.show_message("Program Execution", result)

def main():
    log_action("AdminToolbox application started")
    root = tk.Tk()
    AdminToolboxGUI(root)
    root.mainloop()
    log_action("AdminToolbox application closed")

if __name__ == "__main__":
    main()