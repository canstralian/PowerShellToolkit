import logging
import subprocess
import tempfile
import os

# Configure logging
logging.basicConfig(filename='ReconNINJA.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Payload:
    def __init__(self, name, payload_type, content):
        self.name = name
        self.type = payload_type
        self.content = content

def create_payload(name, payload_type, content):
    """Create a new payload."""
    payload = Payload(name, payload_type, content)
    logging.info(f"Created payload: {name} ({payload_type})")
    return payload

def save_payload(payload):
    """Save payload to a file."""
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=f"_{payload.name}") as temp:
            temp.write(payload.content)
        logging.info(f"Saved payload {payload.name} to {temp.name}")
        return temp.name
    except Exception as e:
        logging.error(f"Error saving payload: {str(e)}")
        return None

def test_payload(payload, target_ip):
    """Test the payload against a target."""
    file_path = save_payload(payload)
    if not file_path:
        return "Failed to save payload for testing"

    try:
        if payload.type == "bash":
            result = subprocess.run(['bash', file_path], capture_output=True, text=True, timeout=30)
        elif payload.type == "python":
            result = subprocess.run(['python', file_path], capture_output=True, text=True, timeout=30)
        else:
            return f"Unsupported payload type: {payload.type}"

        logging.info(f"Tested payload {payload.name} against {target_ip}")
        return f"Payload test result:\nStdout: {result.stdout}\nStderr: {result.stderr}"
    except subprocess.TimeoutExpired:
        return "Payload execution timed out"
    except Exception as e:
        logging.error(f"Error testing payload: {str(e)}")
        return f"Error testing payload: {str(e)}"
    finally:
        os.unlink(file_path)

def list_payloads():
    """List all available payloads."""
    # In a real-world scenario, this would fetch payloads from a database or file system
    return [
        {"name": "Test Bash Payload", "type": "bash"},
        {"name": "Test Python Payload", "type": "python"}
    ]

def get_payload_content(name):
    """Get the content of a specific payload."""
    # This is a simplified version. In a real-world scenario, this would fetch from a database or file system
    payloads = {
        "Test Bash Payload": "#!/bin/bash\necho 'This is a test bash payload'",
        "Test Python Payload": "print('This is a test Python payload')"
    }
    return payloads.get(name, "Payload not found")

def run_payload_framework():
    """Main function to run the payload framework."""
    logging.info("Starting payload framework")
    payloads = list_payloads()
    print("Available payloads:")
    for payload in payloads:
        print(f"- {payload['name']} ({payload['type']})")

    # For demonstration, let's create and test a payload
    test_payload_name = "Test Python Payload"
    test_payload_content = get_payload_content(test_payload_name)
    payload = create_payload(test_payload_name, "python", test_payload_content)
    result = test_payload(payload, "localhost")
    print(f"Test result for {test_payload_name}:")
    print(result)

if __name__ == "__main__":
    run_payload_framework()
