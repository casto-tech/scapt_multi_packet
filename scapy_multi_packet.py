from scapy.all import *
import sys


def send_spoofed_packets(dst_ip, dst_mac, src_ip, src_mac, dst_port=80, count=25):
    """
    Sends TCP packets with spoofed MAC and IP addresses.
    
    Parameters:
    - dst_ip: Destination IP address (e.g., "192.168.1.100")
    - dst_mac: Destination MAC address (e.g., "00:11:22:33:44:55")
    - src_ip: Spoofed source IP address (e.g., "10.0.0.1")
    - src_mac: Spoofed source MAC address (e.g., "aa:bb:cc:dd:ee:ff")
    - dst_port: Destination port (default: 80)
    - count: Number of packets to send (default: 25)
    """
    try:
        # Craft the packet
        packet = (Ether(src=src_mac, dst=dst_mac) /
                  IP(src=src_ip, dst=dst_ip) /
                  TCP(sport=RandShort(), dport=dst_port, flags="S"))

        # Show packet details (optional, for verification)
        packet.show()

        # Send packets at layer 2
        print(f"Sending {count} spoofed packets to {dst_ip}...")
        sendp(packet, count=count, verbose=True)

        print("Packets sent successfully.")

    except PermissionError:
        print("Error: Run this script with root/admin privileges (e.g., sudo).")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # Configuration
    DST_IP = "192.168.86.32"  # Replace with target IP
    DST_MAC = "00:11:22:33:44:55"  # Replace with target MAC
    SRC_IP = "10.0.0.1"  # Spoofed source IP
    SRC_MAC = "aa:bb:cc:dd:ee:ff"  # Spoofed source MAC
    DST_PORT = 80  # Target port (e.g., HTTP)
    COUNT = 25  # Number of packets

    # Ethical use reminder
    print("WARNING: Ensure you have permission to send packets to the target.")
    print("Spoofing without authorization may be illegal.")

    # Send the packets
    send_spoofed_packets(DST_IP, DST_MAC, SRC_IP, SRC_MAC, DST_PORT, COUNT)