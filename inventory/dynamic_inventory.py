#!/usr/bin/python3
import requests
import json
import sys
import os
import time
import re
import csv
import logging

# ========== CONFIG ==========
API_URL = "http://192.168.153.100:....."
INPUT_IP_FILE = "input_ips.csv"
API_CALL_DELAY = 5.0

# ========== SETUP LOGGING ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    stream=sys.stderr
)

# ========== UTILITIES ==========
def is_valid_ip(ip):
    return re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", ip)

def load_ip_user_map():
    ip_user_map = {}
    if not os.path.exists(INPUT_IP_FILE):
        logging.error(f"Input file not found: {INPUT_IP_FILE}")
        return ip_user_map

    with open(INPUT_IP_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ip = row.get("ip", "").strip()
            username = row.get("username", "").strip()

            if not ip or not username:
                logging.warning(f"Missing ip or username in row: {row}")
                continue

            if is_valid_ip(ip):
                ip_user_map[ip] = username
            else:
                logging.warning(f"Invalid IP format in CSV: {ip}")
    return ip_user_map

# ========== INVENTORY FETCH ==========
def fetch_host_data():
    hosts = {}
    ip_user_map = load_ip_user_map()
    for ip, username in ip_user_map.items():
        try:
            response = requests.get(
                API_URL,
                params={'ip': ip, 'username': username},
                timeout=3
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    password = data.get("message")
                    if not password:
                        logging.warning(f"Empty password for IP {ip}")
                        continue

                    hosts[ip] = {
                        "ansible_host": ip,
                        "ansible_user": username,
                        "ansible_ssh_pass": password,
                        "ansible_become_password": password,
                    }
                else:
                    logging.warning(
                        f"API returned code != 200 for {ip}: {data}")
            else:
                logging.warning(
                    f"HTTP error for {ip}: {response.status_code} {response.text}")

        except Exception as e:
            logging.error(f"Exception for IP {ip}: {e}")
        time.sleep(API_CALL_DELAY)
    return hosts

def generate_inventory():
    hostvars = fetch_host_data()
    return {
        "all": {
            "hosts": list(hostvars.keys()),
            "vars": {}
        },
        "_meta": {
            "hostvars": hostvars
        }
    }

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        try:
            inventory = generate_inventory()
            print(json.dumps(inventory, indent=2))
        except Exception as e:
            logging.error(f"Failed to generate inventory: {e}")
            print(json.dumps({}))
    else:
        print(json.dumps({}))

if __name__ == "__main__":
    main()