import scratcher
import capsolver
import random

CAPSOLVER_KEY = "YOUR_CAPSOLVER_KEY" 
CAPSOLVER = capsolver.Capsolver(CAPSOLVER_KEY)

emails = open("emails.txt", "r").read().splitlines()
proxies = open("proxies.txt", "r").read().splitlines()

def get_proxy():
    if len(proxies) == 0:
        return None
    
    return random.choice(proxies)

for email in emails:
    proxy = get_proxy()
    try:
        result = scratcher.make_account_and_spin(email, CAPSOLVER, proxy)

        if result:
            print(f"Created account for {email} and won {result[2]} worth {result[3]} NOK")
        else:
            print(f"Created account for {email} but did not win")
    except Exception as e:
        print(f"Failed to create account for {email} with proxy {proxy}: {e}")
