import os
import argparse
from dotenv import load_dotenv

load_dotenv()

# ... existing imports and code ...

from scripts.ntfy_notifier import send_ntfy_notification

def main():
    parser = argparse.ArgumentParser()
    # ... existing args ...
    args = parser.parse_args()

    try:
        # existing generation logic ...
        print("Generation successful")
        send_ntfy_notification("Success", "Content generation completed successfully", "green")
    except Exception as e:
        error_msg = f"Error in generate_and_update: {str(e)}"
        print(error_msg)
        send_ntfy_notification("Error in Income Bot", error_msg, "warning")
        raise

if __name__ == "__main__":
    main()