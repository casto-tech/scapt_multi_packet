from scapy.all import *
import sys
import argparse


def send_spoofed_packets(dst_ip, dst_mac, src_ip, src_mac, dst_port=80, count=25, iface=None, inter=0):
    try:
        packet = (Ether(src=src_mac, dst=dst_mac) /
                  IP(src=src_ip, dst=dst_ip) /
                  TCP(sport=RandShort(), dport=dst_port, flags="S"))

        packet.show()

        iface = iface or conf.iface
        print(f"Sending {count} spoofed packets to {dst_ip}:{dst_port} via {iface} (inter={inter}s)...")
        sendp(packet, iface=iface, count=count, inter=inter, verbose=True)

        print("Packets sent successfully.")

    except PermissionError:
        print("Error: Run this script with root/admin privileges (e.g., sudo).")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send TCP SYN packets with spoofed MAC and IP addresses.",
        epilog="WARNING: Use only on networks you are authorized to test."
    )
    parser.add_argument("--dst-ip",  required=True,  help="Target IP address")
    parser.add_argument("--dst-mac", required=True,  help="Target MAC address (e.g. 00:11:22:33:44:55)")
    parser.add_argument("--src-ip",  required=True,  help="Spoofed source IP address")
    parser.add_argument("--src-mac", required=True,  help="Spoofed source MAC address (e.g. aa:bb:cc:dd:ee:ff)")
    parser.add_argument("--dst-port", type=int, default=80,   help="Target port (default: 80)")
    parser.add_argument("--count",    type=int, default=25,   help="Number of packets to send (default: 25)")
    parser.add_argument("--iface",                             help="Network interface to send on (default: Scapy's default)")
    parser.add_argument("--inter",    type=float, default=0,   help="Seconds between packets (default: 0)")

    args = parser.parse_args()

    print("WARNING: Ensure you have permission to send packets to the target.")
    print("Spoofing without authorization may be illegal.\n")

    send_spoofed_packets(
        dst_ip=args.dst_ip,
        dst_mac=args.dst_mac,
        src_ip=args.src_ip,
        src_mac=args.src_mac,
        dst_port=args.dst_port,
        count=args.count,
        iface=args.iface,
        inter=args.inter,
    )