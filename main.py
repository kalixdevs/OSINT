import requests
import json

# --------------------------------
# 1. USERNAME CHECKER
# --------------------------------

def check_usernames(username):
    print("\n[+] Checking Username Across Sites")
    sites = {
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
    }

    for site, url in sites.items():
        r = requests.get(url)
        if r.status_code == 200:
            print(f"[FOUND] {site}: {url}")
        else:
            print(f"[NOT FOUND] {site}")

# --------------------------------
# 2. EMAIL BREACH CHECK
# --------------------------------

def check_email_breach(email):
    print("\n[+] Checking Email Breach (HaveIBeenPwned)")

    headers = {
        'User-Agent': 'OSINT-Script',
        'hibp-api-key': 'YOUR_HIBP_API_KEY'  # You must replace this!
    }

    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        breaches = res.json()
        print(f"[!] Breached in {len(breaches)} site(s):")
        for b in breaches:
            print(f" - {b['Name']}")
    elif res.status_code == 404:
        print("[✓] No breach found.")
    else:
        print("[!] Error checking breach.")

# --------------------------------
# 3. DOMAIN/IP INFO
# --------------------------------

def lookup_ip_info(ip_or_domain):
    print("\n[+] Getting IP/Domain Info")
    res = requests.get(f"https://ipinfo.io/{ip_or_domain}/json")
    if res.status_code == 200:
        data = res.json()
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print("[!] Failed to retrieve IP info.")

# --------------------------------
# 4. Passive Recon with Shodan
# --------------------------------

def shodan_lookup(ip, api_key):
    print("\n[+] Shodan Lookup")
    try:
        import shodan
    except ImportError:
        print("Install shodan first with `pip install shodan`")
        return

    api = shodan.Shodan(api_key)
    try:
        result = api.host(ip)
        print(f"IP: {result['ip_str']}")
        print(f"Org: {result.get('org', 'N/A')}")
        print(f"OS: {result.get('os', 'N/A')}")
        for item in result['data']:
            print(f"Port: {item['port']}, Banner: {item['data'][:100]}")
    except shodan.APIError as e:
        print(f"[!] Shodan error: {e}")

# --------------------------------
# MAIN FUNCTION
# --------------------------------

if __name__ == "__main__":
    username = input("Enter username to search: ")
    check_usernames(username)

    email = input("\nEnter email to check breach: ")
    check_email_breach(email)

    target = input("\nEnter IP or domain to lookup: ")
    lookup_ip_info(target)

    run_shodan = input("\nDo Shodan lookup? (y/n): ")
    if run_shodan.lower() == 'y':
        api_key = input("Enter your Shodan API key: ")
        shodan_lookup(target, api_key)
