import logging
import subprocess
import re
from scapy.all import sniff, IP

# Configure logging
logging.basicConfig(filename='ReconNINJA.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_connected_devices():
    """Get a list of connected devices on the network."""
    try:
        # This command works on most Unix-like systems
        arp_output = subprocess.check_output(["arp", "-a"]).decode()
        devices = re.findall(r"((?:\d{1,3}\.){3}\d{1,3})", arp_output)
        return devices
    except Exception as e:
        logging.error(f"Error getting connected devices: {str(e)}")
        return []

def analyze_packet(packet):
    """Analyze a single packet for potential security issues."""
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet[IP].proto
        
        # Example analysis (expand based on specific needs)
        if protocol == 6:  # TCP
            logging.info(f"TCP communication: {src_ip} -> {dst_ip}")
        elif protocol == 17:  # UDP
            logging.info(f"UDP communication: {src_ip} -> {dst_ip}")
        
        # Add more protocol-specific analysis here

def start_packet_capture(duration=60):
    """Start capturing and analyzing network packets."""
    logging.info(f"Starting packet capture for {duration} seconds")
    try:
        sniff(prn=analyze_packet, store=0, timeout=duration)
    except Exception as e:
        logging.error(f"Error during packet capture: {str(e)}")

def analyze_device_communications():
    """Main function to analyze device communications."""
    devices = get_connected_devices()
    logging.info(f"Connected devices: {devices}")
    
    for device in devices:
        logging.info(f"Analyzing communications for device: {device}")
        # You might want to filter packets for specific devices here
    
    start_packet_capture()
    
    # After capture, you could add more analysis, such as:
    # - Identifying unusual communication patterns
    # - Detecting potential malware communication
    # - Checking for unencrypted data transmission
    
    return {"devices": devices, "analysis_complete": True}

if __name__ == "__main__":
    analyze_device_communications()
