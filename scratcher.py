import tls_client

import names
import random
import enum

class URLS(enum.Enum):
    SITE = "https://game.scratcher.io/no-royal-spin?embed=true"
    VISIT = "https://game.scratcher.io/no-royal-spin/visit"
    REGISTER = "https://game.scratcher.io/no-royal-spin/register"
    FINISH = "https://game.scratcher.io/no-royal-spin/finish"

site_key = "6Le-W50UAAAAAKdxq73lhyctA52Pjy4h9laii4Tr"

def create_session(proxy=None):
    session = tls_client.Session(client_identifier="chrome_120", random_tls_extension_order=True)
    session.headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,no;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://game.scratcher.io",
        "Referer": "https://game.scratcher.io/no-royal-spin?embed=true",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }

    if proxy:
        session.proxies = {
            "https": proxy,
            "http": proxy,
        }

    return session

def make_account_and_spin(email, CAPSOLVER, proxy=None):
    session =  create_session(proxy)

    # Unsure if this is needed
    # Inits cookies
    session.get(URLS.SITE.value)

    # Start session and fetch visit ID (token)
    response = session.post(URLS.VISIT.value, json={"s_source": None})
    token = response.json()["token"]


    # Get data for registration
    solution = CAPSOLVER.solve_recap_v2(site_key, URLS.SITE.value)["gRecaptchaResponse"]
    full_name = names.get_full_name()

    payload = {
        "token": token,
        "full_name": full_name,
        "email": email,
        "g-recaptcha-response": solution,
        "cb_competition_terms_and_conditions": "1",
        "cb_kongelige_tilbud": "1",
        "cb_aldersgrensen": "1",
        "__qp_": {"embed": "true"},
        "s_source": None
    }

    response = session.post(URLS.REGISTER.value, json=payload)
    res_json = response.json()

    if ("status" in res_json and res_json["status"] == "error"):
        raise Exception(res_json["message"])


    # spin payload
    payload = {
        "data": {"playing_time": int(5000 + 30000 * random.random())},
        "token": token,
        "s_source": None
    }

    response = session.post(URLS.FINISH.value, json=payload)
    res_json = response.json()

    if (res_json["winner"]):
        return email, res_json["prize_id"], res_json["prize_name"], res_json["prize_value"]
    else:
        return None
