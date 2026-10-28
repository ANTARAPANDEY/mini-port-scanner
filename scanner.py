#!/usr/bin/env python3
"""Mini Port Scanner - a simple TCP connect scanner built with Python sockets.

Only scan systems you own or have permission to test.
"""

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


def scan_port(host, port, timeout):
    """Return True if the TCP port is open on the host."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((host, port)) == 0
    except OSError:
        return False


def get_service(port):
    """Return the common service name for a port, or 'unknown'."""
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "unknown"


def parse_args():
    parser = argparse.ArgumentParser(description="Simple TCP port scanner")
    parser.add_argument("target", help="IP address or hostname to scan")
    parser.add_argument("-s", "--start", type=int, default=1, help="first port (default 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="last port (default 1024)")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="seconds to wait per port (default 0.5)")
    parser.add_argument("-w", "--workers", type=int, default=100, help="parallel threads (default 100)")
    return parser.parse_args()


def main():
    args = parse_args()

    if not (1 <= args.start <= args.end <= 65535):
        sys.exit("Error: ports must satisfy 1 <= start <= end <= 65535")

    try:
        ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        sys.exit(f"Error: could not resolve host '{args.target}'")

    print("-" * 50)
    print(f"Target : {args.target} ({ip})")
    print(f"Ports  : {args.start}-{args.end}")
    print(f"Started: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print("-" * 50)

    ports = range(args.start, args.end + 1)
    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            results = list(pool.map(lambda p: scan_port(ip, p, args.timeout), ports))
    except KeyboardInterrupt:
        sys.exit("\nScan cancelled by user.")

    open_ports = [p for p, is_open in zip(ports, results) if is_open]

    if open_ports:
        print(f"{'PORT':<10}{'STATE':<10}SERVICE")
        for p in open_ports:
            print(f"{p:<10}{'open':<10}{get_service(p)}")
    else:
        print("No open ports found in this range.")

    print("-" * 50)
    print(f"Scan complete: {len(open_ports)} open port(s) out of {len(results)} scanned.")


if __name__ == "__main__":
    main()
