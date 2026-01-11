import requests
import os
from bs4 import BeautifulSoup


URL = "https://shop.amul.com/en/product/amul-high-protein-rose-lassi-200-ml-or-pack-of-30"


RESEND_API_KEY = os.environ["RESEND_API_KEY"]
TO_EMAIL = os.environ["TO_EMAIL"]


FROM_EMAIL = "onboarding@resend.dev"

STATUS_FILE = "last_status.txt"

def send_email():
    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "from": FROM_EMAIL,
            "to": TO_EMAIL,
            "subject": "🟢 Amul High Protein Rose Lassi IN STOCK",
            "html": f"""
                <h3>Amul High Protein Rose Lassi is BACK 🥛</h3>
                <p><b>Pack of 30 (200 ml)</b> is now <b>IN STOCK</b>.</p>
                <p><a href="{URL}">Buy Now</a></p>
            """
        },
        timeout=20
    )
    response.raise_for_status()

def get_last_status():
    if not os.path.exists(STATUS_FILE):
        return "unknown"
    return open(STATUS_FILE).read().strip()

def save_status(status):
    with open(STATUS_FILE, "w") as f:
        f.write(status)

headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(URL, headers=headers, timeout=20)
soup = BeautifulSoup(r.text, "html.parser")
text = soup.get_text().lower()

in_stock = "add to cart" in text and "sold out" not in text
last_status = get_last_status()

if in_stock and last_status != "in_stock":
    send_email()
    save_status("in_stock")
elif not in_stock:
    save_status("out_of_stock")
