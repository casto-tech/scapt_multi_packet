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
```

### Virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate
pip install scapy
```

> **Note:** When using a venv, `sudo` won't see it by default. Run with the full path to the venv Python:
> ```bash
> sudo ~/Git/scapt_multi_packet/venv/bin/python3 scapy_multi_packet.py [args]
> ```

---

## Usage

All parameters are passed as command-line arguments — no need to edit the script.

```
sudo python3 scapy_multi_packet.py \
  --dst-ip  <target IPv4>        (required) \
  --dst-mac <target MAC>         (required) \
  --src-ip  <spoofed IPv4>       (required) \
  --src-mac <spoofed MAC>        (required) \
  [--dst-port <1–65535>]         default: 80 \
  [--count   <n>]                default: 25 \
  [--flags   <TCP flags>]        default: S \
  [--iface   <interface name>]   default: Scapy auto-selects \
  [--inter   <seconds>]          default: 0
```

Built-in help:

```bash
sudo python3 scapy_multi_packet.py --help
```

---

## Arguments

| Argument | Required | Type | Default | Description |
|---|---|---|---|---|
| `--dst-ip` | Yes | IPv4 | — | Target IP address |
| `--dst-mac` | Yes | MAC | — | Target MAC address |
| `--src-ip` | Yes | IPv4 | — | Spoofed source IP address |
| `--src-mac` | Yes | MAC | — | Spoofed source MAC address |
| `--dst-port` | No | int 1–65535 | `80` | Target TCP port |
| `--count` | No | int | `25` | Number of packets to send |
| `--flags` | No | string | `S` | TCP flags (see [TCP Flags](#tcp-flags)) |
| `--iface` | No | string | Scapy default | Network interface to send on |
| `--inter` | No | float (seconds) | `0` | Delay between packets |

### TCP Flags

Flags are specified as a string of one or more characters. All combinations are valid.

| Flag | Char | Meaning |
|---|---|---|
| SYN | `S` | Connection initiation |
| ACK | `A` | Acknowledgement |
| FIN | `F` | Connection teardown |
| RST | `R` | Reset connection |
| PSH | `P` | Push data immediately |
| URG | `U` | Urgent pointer field significant |
| ECE | `E` | ECN echo |
| CWR | `C` | Congestion window reduced |

Common combinations:

| Flags string | Scan / test type |
|---|---|
| `S` | SYN scan (default) |
| `SA` | SYN-ACK — test stateful firewall rules |
| `F` | FIN scan |
| `R` | RST |
| `FPU` | Xmas scan (FIN + PSH + URG) |
| `FA` | FIN-ACK |

---

## Examples

### Minimal — SYN to port 80

```bash
sudo python3 scapy_multi_packet.py \
  --dst-ip 192.168.1.100 \
  --dst-mac 00:11:22:33:44:55 \
  --src-ip 10.0.0.1 \
  --src-mac aa:bb:cc:dd:ee:ff
```

### Custom port, count, and throttle rate

```bash
sudo python3 scapy_multi_packet.py \
  --dst-ip 192.168.1.100 \
  --dst-mac 00:11:22:33:44:55 \
  --src-ip 10.0.0.1 \
  --src-mac aa:bb:cc:dd:ee:ff \
  --dst-port 443 \
  --count 50 \
  --inter 0.5
```

### FIN scan

```bash
sudo python3 scapy_multi_packet.py \
  --dst-ip 192.168.1.100 \
  --dst-mac 00:11:22:33:44:55 \
  --src-ip 10.0.0.1 \
  --src-mac aa:bb:cc:dd:ee:ff \
  --dst-port 22 \
  --flags F \
  --count 5
```

### Xmas scan (FIN + PSH + URG)

```bash
sudo python3 scapy_multi_packet.py \
  --dst-ip 192.168.1.100 \
  --dst-mac 00:11:22:33:44:55 \
  --src-ip 10.0.0.1 \
  --src-mac aa:bb:cc:dd:ee:ff \
  --dst-port 80 \
  --flags FPU \
  --count 5
```

### Explicit network interface

```bash
sudo python3 scapy_multi_packet.py \
  --dst-ip 192.168.1.100 \
  --dst-mac 00:11:22:33:44:55 \
  --src-ip 10.0.0.1 \
  --src-mac aa:bb:cc:dd:ee:ff \
  --iface eth0
```

To list available interfaces:

```bash
ip link show
```

---

## Use Cases

All use cases require **explicit authorization** on the target network or system.

### 1. Firewall / IDS rule testing

Verify that a firewall or IDS correctly drops or flags packets from spoofed sources.

```bash
sudo python3 scapy_multi_packet.py \
  --dst-ip 192.168.1.1 \
  --dst-mac aa:bb:cc:dd:ee:01 \
  --src-ip 10.99.99.99 \
  --src-mac de:ad:be:ef:00:01 \
  --dst-port 22 \
  --count 10
```

Expected: packets appear in firewall logs / IDS alerts and are dropped.

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

Expected: monitoring tool logs the spoofed source IP, not the sender's real IP.

---

### 3. Port availability probing (lab environment)

Send SYN packets to observe TCP state-machine behavior on specific ports without completing a full handshake.

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

### 4. SYN flood simulation (authorized, isolated lab only)

Observe how a test server handles connection exhaustion. **Only run on hardware you own and control.**

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

### 5. Stateful firewall bypass testing (SYN-ACK)

Send SYN-ACK packets with a spoofed source to test whether a stateful firewall rejects unsolicited ACKs.

```bash
sudo python3 scapy_multi_packet.py \
  --dst-ip 192.168.1.1 \
  --dst-mac aa:bb:cc:dd:ee:01 \
  --src-ip 10.0.0.1 \
  --src-mac aa:bb:cc:dd:ee:ff \
  --dst-port 443 \
  --flags SA \
  --count 5
```

---

### 6. Throttled testing (rate-limited send)

Send packets slowly to avoid overwhelming a test target or triggering rate-based IDS rules — useful when testing detection thresholds.

```bash
sudo python3 scapy_multi_packet.py \
  --dst-ip 192.168.1.100 \
  --dst-mac 00:11:22:33:44:55 \
  --src-ip 10.0.0.1 \
  --src-mac aa:bb:cc:dd:ee:ff \
  --dst-port 80 \
  --count 100 \
  --inter 1.0
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
        flags="S",
        count=1,
        inter=0.5,
    )
```

Full function signature:

```python
send_spoofed_packets(
    dst_ip,           # str — target IPv4
    dst_mac,          # str — target MAC
    src_ip,           # str — spoofed source IPv4
    src_mac,          # str — spoofed source MAC
    dst_port=80,      # int — target TCP port
    count=25,         # int — number of packets
    iface=None,       # str | None — network interface (None = Scapy default)
    inter=0,          # float — seconds between packets
    flags="S",        # str — TCP flags
)
```

---

## How it works

The script stacks three Scapy layers into a single packet and transmits it at Layer 2:

```
Ether(src=src_mac, dst=dst_mac)        ← Layer 2: spoofed MAC addresses
  / IP(src=src_ip, dst=dst_ip)         ← Layer 3: spoofed IP addresses
  / TCP(sport=RandShort(),             ← Layer 4: random ephemeral source port
        dport=dst_port,                           configurable dest port
        flags=flags)                              configurable TCP flags
```

`sendp()` sends at Layer 2 (raw Ethernet), bypassing the OS TCP/IP stack entirely. This is why:

- **Root is required** — the OS won't allow raw socket access without it.
- **The source address is fully controllable** — the kernel's own IP stack is not involved, so it can't enforce the real source IP.
- **Responses go to the spoofed source** — if the target replies, the reply goes to `src_ip`, not to the machine running the script.

Input validation runs before any packet is crafted:

- IPv4 addresses are validated with Python's `ipaddress` module.
- MAC addresses are checked against the `xx:xx:xx:xx:xx:xx` format.
- Ports are checked to be in the range 1–65535.
- TCP flags are checked against the set `F S R P A U E C`.

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'scapy'` | `sudo` uses a different Python than your venv | Run `sudo /path/to/venv/bin/python3 scapy_multi_packet.py` |
| `PermissionError` | Not running as root | Prefix the command with `sudo` |
| Packets sent but target never receives them | Wrong `--dst-mac` | Run `arp -n` or `ip neigh` to look up the correct MAC |
| Script hangs or sends on wrong interface | Scapy picked the wrong default interface | Add `--iface eth0` (or `wlan0`, etc.) |
| Replies never arrive back | Spoofed `--src-ip` doesn't route to this machine | Expected — replies go to the spoofed source, not the sender |
| Invalid argument error on `--flags` | Unrecognised flag character | Valid characters are `F S R P A U E C` only |

---

## Warning

> Sending spoofed packets without **explicit written permission** from the network/system owner is illegal in most jurisdictions and violates computer fraud laws (e.g. CFAA in the US, Computer Misuse Act in the UK). This tool is provided strictly for authorized security testing, CTF competitions, and educational lab environments.

---

## Contributing

Fork the repo, make your changes, and open a pull request. Contributions are welcome as long as they adhere to ethical usage standards.

---

## Disclaimer

This code is provided "as is" without warranty of any kind. The author is not responsible for any misuse or damage caused by this script.
