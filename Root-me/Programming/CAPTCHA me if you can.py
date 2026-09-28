import re
import base64
import subprocess
import requests
import urllib3

urllib3.disable_warnings()

URL = "http://challenge01.root-me.org/programmation/ch8/"

def solve():
    session = requests.Session()

    # Get the captcha
    response = session.get(URL, verify=False)

    match = re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', response.text)
    if not match:
        print("[!] No captcha found")
        return False

    image_data = base64.b64decode(match.group(1))

    # Save image temporarily
    with open('/tmp/captcha.png', 'wb') as f:
        f.write(image_data)

    # Run gocr
    result = subprocess.run(['gocr', '-i', '/tmp/captcha.png'],
                          capture_output=True, text=True)
    text = result.stdout.strip()

    # Clean up the result
    text = text.replace('\n', '').replace(' ', '').replace(',', '').replace("'", '')

    print(f"[*] OCR result: '{text}'")

    if not text:
        print("[!] Empty OCR result")
        return False

    # Submit
    submit = session.post(URL, data={'cametu': text}, verify=False)

    # Check response
    clean_text = re.sub(r'<[^>]+>', ' ', submit.text)
    clean_text = ' '.join(clean_text.split())

    if 'Rat' in submit.text or 'retente' in submit.text.lower():
        print(f"[!] Wrong: {clean_text[:100]}")
        return False

    print(f"\n[+] SUCCESS!")
    print(f"[+] {clean_text}")

    # Extract flag
    flag_match = re.search(r'flag\s+est\s+(\S+)', clean_text, re.IGNORECASE)
    if flag_match:
        print(f"\n[+] FLAG: {flag_match.group(1)}")

    return True

def main():
    print("=" * 50)
    print("Root-me Captcha Solver (ch8)")
    print("Using gocr - install with: brew install gocr")
    print("=" * 50)

    for attempt in range(20):
        print(f"\n[Attempt {attempt + 1}/20]")
        if solve():
            break
    else:
        print("\n[!] Failed after 20 attempts")

if __name__ == "__main__":
    main()
