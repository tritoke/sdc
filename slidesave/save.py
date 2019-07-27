import re
from datetime import datetime
from requests import get, head
from time import sleep
import os

BASEPATH = os.getcwd() + os.path.sep


def save(req):
    """
    Attempts to save the content from the supplied
    request: req
    """
    print(f"Saving request of length {len(req.content)} bytes")
    fname = datetime.strftime(datetime.now(), "%F_%H-%M")
    with open(f"{BASEPATH}{fname}.pptx", "wb") as f:
        f.write(request.content)


def parse_id(url):
    """
    Parses the file id from the slides URL
    returns the ID
    """

    search = re.search(r"\S+/d/(?P<id>[^/]*)/.*", url)
    if search:
        return search.group(1)
    else:
        print("Failed to parse the ID from the URL")

        slides_id = input("Enter the ID manually: ")

        while not head(
            f"https://docs.google.com/presentation/d/{slides_id}/export/pptx"
        ):
            print("Wrong ID, please try again below")
            slides_id = input("Enter the ID manually: ")

        return slides_id


def get_backup_time():
    """
    Gets the number of minutes in between backups.
    returns the number of seconds to sleep for between backups.
    """
    while True:
        try:
            mins = float(
                input("Enter the number of minutes between each backup save: ")
            )
            if mins <= 0:
                print("Invalid number of minutes, must be positive.")
            else:
                break
        except ValueError:
            print(
                "Invalid number of minutes, please enter number and nothing else, i.e. 30"
            )
    return int(mins * 60)


print(f"\nSaving backups to {BASEPATH}\n")

original_url = input("Enter page url: ")

slides_id = parse_id(original_url)

url = f"https://docs.google.com/presentation/d/{slides_id}/export/pptx"
print(f"\nDownloading from {url}\n")

request = get(url)

if request:
    save(request)

    secs = get_backup_time()

    backups = 1
    start = datetime.strftime(datetime.now(), "%F %H:%M")
    while True:
        print(f"{backups} since {start}")
        backups += 1
        sleep(secs)
        save(get(url))

else:
    print("Getting page failed, please restart and enter the correct id.")
