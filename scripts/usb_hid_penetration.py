import platform
import logging
import requests

# Configure logging
logging.basicConfig(filename='ReconNINJA.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def identify_usb_hid_devices():
    """
    Identify and list connected USB HID devices.
    """
    devices = []
    
    try:
        if platform.system() == "Windows":
            import win32com.client
            wmi = win32com.client.GetObject("winmgmts:")
            for usb in wmi.InstancesOf("Win32_USBControllerDevice"):
                devices.append(usb.Dependent.Caption)
        elif platform.system() == "Linux":
            import pyudev
            context = pyudev.Context()
            for device in context.list_devices(subsystem='input'):
                if device.get('ID_INPUT_KEYBOARD', 0) == "1" or device.get('ID_INPUT_MOUSE', 0) == "1":
                    devices.append(device.get('NAME', 'Unknown HID Device'))
        else:
            logging.warning(f"Unsupported operating system: {platform.system()}")
            return None
        
        logging.info(f"Identified {len(devices)} USB HID devices")
        return devices
    except Exception as e:
        logging.error(f"Error identifying USB HID devices: {str(e)}")
        return None

def check_cve_database(device_name):
    """
    Check CVE database for vulnerabilities related to the device.
    """
    try:
        # Using the NIST NVD API for CVE lookup
        base_url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
        params = {
            "keyword": device_name,
            "resultsPerPage": 10
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        cve_data = response.json()
        vulnerabilities = cve_data.get('result', {}).get('CVE_Items', [])
        
        logging.info(f"Found {len(vulnerabilities)} potential vulnerabilities for {device_name}")
        return vulnerabilities
    except Exception as e:
        logging.error(f"Error checking CVE database: {str(e)}")
        return None

# Main function to run the USB HID penetration testing module
def run_usb_hid_pentest():
    devices = identify_usb_hid_devices()
    if devices:
        for device in devices:
            print(f"Identified device: {device}")
            vulnerabilities = check_cve_database(device)
            if vulnerabilities:
                print(f"Potential vulnerabilities for {device}:")
                for vuln in vulnerabilities:
                    cve_id = vuln['cve']['CVE_data_meta']['ID']
                    description = vuln['cve']['description']['description_data'][0]['value']
                    print(f"- {cve_id}: {description[:100]}...")
            else:
                print(f"No known vulnerabilities found for {device}")
    else:
        print("No USB HID devices identified or an error occurred.")

if __name__ == "__main__":
    run_usb_hid_pentest()
