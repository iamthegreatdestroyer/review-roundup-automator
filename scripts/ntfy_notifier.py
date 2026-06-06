import os
import requests
from dotenv import load_dotenv

def send_ntfy_notification(title: str, message: str, tags: str = "warning"):
    load_dotenv()
    ntfy_topic = os.getenv('NTFY_TOPIC')
    if not ntfy_topic:
        print("NTFY_TOPIC not set in .env - skipping notification")
        return

    url = f"https://ntfy.sh/{ntfy_topic}"
    requests.post(url, data=message, headers={
        "Title": title,
        "Tags": tags,
        "Priority": "default"
    })

if __name__ == "__main__":
    send_ntfy_notification("Test Notification", "ntfy integration working for autonomous income projects!")