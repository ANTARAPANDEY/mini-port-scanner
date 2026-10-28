# Mini Port Scanner

A simple multithreaded TCP port scanner written in Python using the standard `socket` library. It checks which ports are open on a target host and shows the common service name for each one.

## Features
- Configurable port range (`-s` / `-e`)
- Adjustable socket timeout (`-t`)
- Multithreaded scanning (`-w`) for faster results
- Error handling for unresolvable hosts, bad port ranges and closed or filtered ports
- Clean, structured output

## Requirements
- Python 3.8+ (no external libraries)

## Usage
```bash
python scanner.py <target> [-s START] [-e END] [-t TIMEOUT] [-w WORKERS]
```

Examples:
```bash
python scanner.py 127.0.0.1
python scanner.py 127.0.0.1 -s 1 -e 9000 -t 0.3
python scanner.py scanme.nmap.org -s 20 -e 100
```

## Sample output
```
--------------------------------------------------
Target : 127.0.0.1 (127.0.0.1)
Ports  : 1-9000
Started: 2026-10-28 18:30:00
--------------------------------------------------
PORT      STATE     SERVICE
8000      open      unknown
--------------------------------------------------
Scan complete: 1 open port(s) out of 9000 scanned.
```

## How it works
For each port the scanner tries a full TCP connection (`connect_ex`). A return value of `0` means the connection succeeded, so the port is open. Threads let many ports be checked at once.

## Legal notice
Only scan systems you own or have explicit permission to test. `scanme.nmap.org` is provided by the Nmap project for practice scanning. Unauthorised scanning may be illegal.

## Author
Antara Pandey
