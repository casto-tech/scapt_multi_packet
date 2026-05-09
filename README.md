# Spoofed Packet Sender

A Python script for crafting and sending TCP packets with spoofed MAC and IP addresses using the [Scapy](https://scapy.net/) library. Intended for **educational and authorized testing purposes only**.

---

## Requirements

- Python 3.x
- Scapy 2.5.x or later
- Root / administrator privileges (required for raw packet injection)

---

## Installation

### Standard install

```bash
pip install scapy
sudo python3 scapy_multi_packet.py
```

### Virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate
pip install scapy

# Run using the venv Python so sudo picks up the right interpreter
sudo ~/Git/scapt_multi_packet/venv/bin/python3 scapy_multi_packet.py
```

---

## Usage

All arguments are passed on the command line — no need to edit the script.

```
sudo python3 scapy_multi_packet.py \
  --dst-ip  <target IP>   \
  --dst-mac <target MAC>  \
  --src-ip  <spoofed IP>  \
  --src-mac <spoofed MAC> \
  [--dst-port <port>]     \   # default: 80
  [--count <n>]           \   # default: 25
  [--iface <interface>]       # default: Scapy's auto-selected interface
```

**Quick example:**

```bash
sudo python3 scapy_multi_packet.py \
  --dst-ip 192.168.1.100 \
  --dst-mac 00:11:22:33:44:55 \
  --src-ip 10.0.0.1 \
  --src-mac aa:bb:cc:dd:ee:ff \
  --dst-port 443 \
  --count 10
```

Built-in help:

```bash
sudo python3 scapy_multi_packet.py --help
```

---

## Use Cases

All use cases require **explicit authorization** on the target network or system.

### 1. Firewall / IDS rule testing

Verify that your firewall or intrusion detection system correctly drops or flags SYN packets arriving from spoofed sources.

```bash
sudo python3 scapy_multi_packet.py \
  --dst-ip 192.168.1.1 \
  --dst-mac aa:bb:cc:dd:ee:01 \
  --src-ip 10.99.99.99 \
  --src-mac de:ad:be:ef:00:01 \
  --dst-port 22 \
  --count 10
```

Expected result: packets appear in firewall logs / IDS alerts; traffic is dropped.

---

### 2. Network monitoring / SIEM validation

Confirm that your SIEM or packet capture pipeline records spoofed-source traffic correctly.

```bash
sudo python3 scapy_multi_packet.py \
  --dst-ip 192.168.1.50 \
  --dst-mac aa:bb:cc:dd:ee:02 \
  --src-ip 172.16.0.200 \
  --src-mac ca:fe:ba:be:00:02 \
  --dst-port 443 \
  --count 5
```

Check that your monitoring tool logs the correct source IP, not the sender's real IP.

---

### 3. Port availability probing (lab environment)

Send SYN packets to probe which ports on a lab host respond — useful when you control both ends and want to observe TCP state-machine behavior without a full connection.

```bash
sudo python3 scapy_multi_packet.py \
  --dst-ip 192.168.1.200 \
  --dst-mac aa:bb:cc:dd:ee:03 \
  --src-ip 192.168.1.201 \
  --src-mac de:ad:be:ef:00:03 \
  --dst-port 8080 \
  --count 1
```

---

### 4. Stress / load simulation (authorized)

Flood a test server with SYN packets to observe how it handles connection exhaustion (SYN flood simulation). **Only run on isolated lab hardware you own.**

```bash
sudo python3 scapy_multi_packet.py \
  --dst-ip 10.0.0.5 \
  --dst-mac aa:bb:cc:dd:ee:04 \
  --src-ip 10.0.0.99 \
  --src-mac ba:dc:af:eb:ad:04 \
  --dst-port 80 \
  --count 1000
```

---

## Using the function directly (scripting / automation)

`send_spoofed_packets()` can be imported and called from your own scripts for more advanced workflows:

```python
from scapy_multi_packet import send_spoofed_packets

# Loop over multiple ports
for port in [22, 80, 443, 8080]:
    send_spoofed_packets(
        dst_ip="192.168.1.100",
        dst_mac="00:11:22:33:44:55",
        src_ip="10.0.0.1",
        src_mac="aa:bb:cc:dd:ee:ff",
        dst_port=port,
        count=1
    )
```

---

## How it works

The script stacks three Scapy layers into a single packet:

```
Ether(src=src_mac, dst=dst_mac)   ← Layer 2: spoofed MAC addresses
  / IP(src=src_ip, dst=dst_ip)    ← Layer 3: spoofed IP addresses
  / TCP(sport=RandShort(),         ← Layer 4: random source port, SYN flag
        dport=dst_port, flags="S")
```

`sendp()` transmits at Layer 2 (raw Ethernet), bypassing the OS TCP/IP stack entirely — which is why root privileges are required and why the source address is fully controllable.

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'scapy'` | sudo uses a different Python | Run `sudo /path/to/venv/bin/python3 scapy_multi_packet.py` |
| `PermissionError` | Not running as root | Prefix with `sudo` |
| Packets sent but target never receives them | Wrong `DST_MAC` | Use `arp -n` or `ip neigh` to find the correct MAC |
| No output / script hangs | Interface busy or wrong iface | Add `--iface eth0` (or `wlan0`, etc.) to the command |

---

## Warning

> Sending spoofed packets without **explicit written permission** from the network/system owner is illegal in most jurisdictions and violates computer fraud laws. This tool is provided strictly for authorized security testing, CTF competitions, and educational lab environments.

---

## Contributing

Fork the repo, make your changes, and open a pull request. Contributions are welcome as long as they adhere to ethical usage standards.

---

## Disclaimer

This code is provided "as is" without warranty of any kind. The author is not responsible for any misuse or damage caused by this script.
