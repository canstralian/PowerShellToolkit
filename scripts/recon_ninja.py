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
from scripts.a2c_wifi_learner import WiFiEnvironment, A2CAgent, capture_pcap, passive_sniff, active_deauth

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

@app.route('/api/duckyscript_payloads', methods=['GET'])
def get_duckyscript_payloads():
    try:
        logging.info("Retrieving list of DuckyScript payloads")
        payloads = list_duckyscript_payloads()
        return jsonify({"success": True, "payloads": payloads})
    except Exception as e:
        logging.error(f"Error listing DuckyScript payloads: {str(e)}")
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

@app.route('/api/a2c_wifi_learn', methods=['POST'])
def a2c_wifi_learn():
    try:
        logging.info("Starting A2C WiFi Learning")
        env = WiFiEnvironment()
        state_dim = env.observation_space.shape[0]
        action_dim = env.action_space.n
        agent = A2CAgent(state_dim, action_dim)
        
        num_episodes = int(request.json.get('num_episodes', 100))
        
        results = []
        for episode in range(num_episodes):
            state = env.reset()
            done = False
            total_reward = 0
            
            while not done:
                action = agent.act(state)
                next_state, reward, done, _ = env.step(action)
                agent.train(state, action, reward, next_state, done)
                state = next_state
                total_reward += reward
            
            results.append({"episode": episode + 1, "total_reward": total_reward})
        
        logging.info("A2C WiFi Learning completed successfully")
        return jsonify({"success": True, "results": results})
    except Exception as e:
        logging.error(f"Error during A2C WiFi Learning: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/capture_pcap', methods=['POST'])
def api_capture_pcap():
    try:
        duration = int(request.json.get('duration', 60))
        filename = request.json.get('filename', 'captured_traffic.pcap')
        
        capture_pcap(filename, duration)
        
        return jsonify({"success": True, "message": f"PCAP file saved as {filename}"})
    except Exception as e:
        logging.error(f"Error during PCAP capture: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/passive_sniff', methods=['POST'])
def api_passive_sniff():
    try:
        interface = request.json.get('interface', 'wlan0')
        duration = int(request.json.get('duration', 30))
        
        packets = passive_sniff(interface, duration)
        
        return jsonify({"success": True, "message": f"Sniffed {len(packets)} packets"})
    except Exception as e:
        logging.error(f"Error during passive sniffing: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/active_deauth', methods=['POST'])
def api_active_deauth():
    try:
        target_mac = request.json.get('target_mac')
        gateway_mac = request.json.get('gateway_mac')
        count = int(request.json.get('count', 10))
        interface = request.json.get('interface', 'wlan0')
        
        if not target_mac or not gateway_mac:
            return jsonify({"success": False, "error": "Target MAC and Gateway MAC are required"}), 400
        
        active_deauth(target_mac, gateway_mac, count, interface)
        
        return jsonify({"success": True, "message": f"Sent {count} deauth packets to {target_mac}"})
    except Exception as e:
        logging.error(f"Error during active deauthentication: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logging.info(f"Starting ReconNINJA application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)