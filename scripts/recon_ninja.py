import os
import logging
from flask import Flask, render_template, request, jsonify
from scripts.usb_hid_penetration import run_usb_hid_pentest
from scripts.firmware_analysis import run_firmware_analysis
from scripts.device_communication_analysis import analyze_device_communications
from scripts.payload_framework import create_payload, test_payload, list_payloads, get_payload_content
from scripts.cloud_vulnerability_scan import run_cloud_vulnerability_scan
from scripts.cloud_network_mapping import run_cloud_network_mapping
from scripts.cloud_web_app_security import run_cloud_web_app_security_test
from scripts.duckyscript_payloads import list_duckyscript_payloads, save_duckyscript_payload, execute_duckyscript_payload, get_duckyscript_payload_content

app = Flask(__name__, template_folder='../templates', static_folder='../static')

logging.basicConfig(filename='ReconNINJA.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/usb_hid_pentest', methods=['POST'])
def usb_hid_pentest():
    try:
        logging.info("Starting USB HID penetration test")
        results = run_usb_hid_pentest()
        logging.info("USB HID penetration test completed successfully")
        return jsonify({"success": True, "results": results})
    except Exception as e:
        logging.error(f"Error during USB HID penetration test: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/firmware_analysis', methods=['POST'])
def firmware_analysis():
    try:
        logging.info("Starting firmware analysis")
        if 'firmware' not in request.files:
            logging.error("No firmware file provided")
            return jsonify({"success": False, "error": "No firmware file provided"}), 400
        
        firmware_file = request.files['firmware']
        if firmware_file.filename == '':
            logging.error("No firmware file selected")
            return jsonify({"success": False, "error": "No firmware file selected"}), 400
        
        temp_path = os.path.join('/tmp', firmware_file.filename)
        firmware_file.save(temp_path)
        
        results = run_firmware_analysis(temp_path)
        
        os.remove(temp_path)
        
        logging.info("Firmware analysis completed successfully")
        return jsonify({"success": True, "results": results})
    except Exception as e:
        logging.error(f"Error during firmware analysis: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/device_communication_analysis', methods=['POST'])
def device_communication_analysis():
    try:
        logging.info("Starting device communication analysis")
        results = analyze_device_communications()
        logging.info("Device communication analysis completed successfully")
        return jsonify({"success": True, "results": results})
    except Exception as e:
        logging.error(f"Error during device communication analysis: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/payloads', methods=['GET'])
def get_payloads():
    try:
        logging.info("Retrieving list of payloads")
        payloads = list_payloads()
        return jsonify({"success": True, "payloads": payloads})
    except Exception as e:
        logging.error(f"Error listing payloads: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/payload', methods=['POST'])
def manage_payload():
    try:
        data = request.json
        action = data.get('action')
        
        if action == 'create':
            logging.info(f"Creating new payload: {data.get('name')}")
            name = data.get('name')
            payload_type = data.get('type')
            content = data.get('content')
            payload = create_payload(name, payload_type, content)
            return jsonify({"success": True, "message": f"Payload {name} created successfully"})
        
        elif action == 'test':
            logging.info(f"Testing payload: {data.get('name')}")
            name = data.get('name')
            target_ip = data.get('target_ip', 'localhost')
            content = get_payload_content(name)
            payload_type = next((p['type'] for p in list_payloads() if p['name'] == name), None)
            
            if not content or not payload_type:
                logging.error(f"Payload not found: {name}")
                return jsonify({"success": False, "error": "Payload not found"}), 404
            
            payload = create_payload(name, payload_type, content)
            result = test_payload(payload, target_ip)
            logging.info(f"Payload test completed: {name}")
            return jsonify({"success": True, "result": result})
        
        else:
            logging.error(f"Invalid action: {action}")
            return jsonify({"success": False, "error": "Invalid action"}), 400
    
    except Exception as e:
        logging.error(f"Error managing payload: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/cloud_vulnerability_scan', methods=['POST'])
def cloud_vulnerability_scan():
    try:
        logging.info("Starting cloud-based vulnerability scan")
        target = request.json.get('target')
        results = run_cloud_vulnerability_scan(target)
        logging.info("Cloud-based vulnerability scan completed successfully")
        return jsonify({"success": True, "results": results})
    except Exception as e:
        logging.error(f"Error during cloud-based vulnerability scan: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/cloud_network_mapping', methods=['POST'])
def cloud_network_mapping():
    try:
        logging.info("Starting cloud-based network mapping")
        target = request.json.get('target')
        results = run_cloud_network_mapping(target)
        logging.info("Cloud-based network mapping completed successfully")
        return jsonify({"success": True, "results": results})
    except Exception as e:
        logging.error(f"Error during cloud-based network mapping: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/cloud_web_app_security', methods=['POST'])
def cloud_web_app_security():
    try:
        logging.info("Starting cloud-based web application security testing")
        target = request.json.get('target')
        results = run_cloud_web_app_security_test(target)
        logging.info("Cloud-based web application security testing completed successfully")
        return jsonify({"success": True, "results": results})
    except Exception as e:
        logging.error(f"Error during cloud-based web application security testing: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/duckyscript_payloads', methods=['GET'])
def get_duckyscript_payloads():
    try:
        logging.info("Retrieving list of DuckyScript payloads")
        payloads = list_duckyscript_payloads()
        return jsonify({"success": True, "payloads": payloads})
    except Exception as e:
        logging.error(f"Error listing DuckyScript payloads: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/duckyscript_payload', methods=['POST'])
def manage_duckyscript_payload():
    try:
        data = request.json
        action = data.get('action')
        
        if action == 'create':
            logging.info(f"Creating new DuckyScript payload: {data.get('name')}")
            name = data.get('name')
            content = data.get('content')
            save_duckyscript_payload(name, content)
            return jsonify({"success": True, "message": f"DuckyScript payload {name} created successfully"})
        
        elif action == 'execute':
            logging.info(f"Executing DuckyScript payload: {data.get('name')}")
            name = data.get('name')
            result = execute_duckyscript_payload(name)
            return jsonify({"success": True, "result": result})
        
        elif action == 'get_content':
            logging.info(f"Retrieving content of DuckyScript payload: {data.get('name')}")
            name = data.get('name')
            content = get_duckyscript_payload_content(name)
            if content is None:
                return jsonify({"success": False, "error": "Payload not found"}), 404
            return jsonify({"success": True, "content": content})
        
        else:
            logging.error(f"Invalid action: {action}")
            return jsonify({"success": False, "error": "Invalid action"}), 400
    
    except Exception as e:
        logging.error(f"Error managing DuckyScript payload: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = 5000
    logging.info(f"Starting ReconNINJA application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)