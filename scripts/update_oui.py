import requests
import os
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

OUI_URL = "https://standards-oui.ieee.org/oui/oui.csv"


def get_local_file_date(path):
    if not os.path.exists(path):
        return None

    return datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc)


def get_remote_file_date():
    try:
        response = requests.head(OUI_URL, timeout=5)
        last_modified = response.headers.get("Last-Modified")

        if last_modified:
            return parsedate_to_datetime(last_modified)

    except requests.RequestException:
        pass

    return None


def format_date(dt):
    """Format datetime for display (local timezone)."""
    return dt.astimezone().strftime('%Y-%m-%d %H:%M:%S')


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, "macvendorscli", "oui.csv")

    print("Checking OUI database...\n")

    local_date = get_local_file_date(csv_path)
    remote_date = get_remote_file_date()

  
    if local_date:
        print(f"Local file last update : {format_date(local_date)}")
    else:
        print("Local file not found")

    if remote_date:
        print(f"Remote file last update: {format_date(remote_date)}")
    else:
        print("Could not retrieve remote file date")

    print()

  
    if local_date and remote_date:
        if remote_date <= local_date:
            print("Your OUI database is already up to date ")
            return
        else:
            print("A newer version is available. Updating...\n")
    else:
        print("Proceeding with download...\n")


    try:
        response = requests.get(OUI_URL, timeout=10)
        response.raise_for_status()

  
        if "Assignment" not in response.text:
            print("Downloaded file does not look like a valid OUI CSV ")
            return

    except requests.RequestException as e:
        print(f"Error downloading file: {e}")
        return


    if os.path.exists(csv_path):
        backup_path = csv_path + ".bak"
        try:
            os.replace(csv_path, backup_path)
            print(f"Backup created: {backup_path}")
        except Exception:
            print("Warning: could not create backup")

    try:
        with open(csv_path, "wb") as f:
            f.write(response.content)

        print("OUI database updated successfully! ")
        print(f"Saved to: {csv_path}")

    except Exception as e:
        print(f"Error saving file: {e}")


if __name__ == "__main__":
    main()