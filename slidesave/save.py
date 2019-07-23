import re
from datetime import datetime
from requests import get
from time import sleep

original_url = input("Enter page url: ")
search = re.search(r"\S+/d/(?P<id>.*)/.*", original_url)
if not search:
    print("Couldn't parse id from URL")
    print("The URL should look like https://docs.google.com/presentation/d/<id>/edit/<garbage nobody cares about>")
    print("If it doesn't look like this then you are probably on the wrong page.")
    slides_id = input("Enter ID manually: ")
else:
    slides_id = search.group("id")
url = f"https://docs.google.com/presentation/d/{slides_id}/export/pptx"
request = get(url)
if request:
    open(f"{datetime.strftime(datetime.now(),'%F--%H:%M')}.pptx","wb").write(request.content)
    while True:
        try:
            mins = int(input("Enter the number of minutes between each backup save: "))
            if mins <= 0:
                print("Invalid number of minutes, must be a positive integer.")
            else:
                break
        except ValueError:
            print("Invalid number of minutes, please enter number and nothing else, i.e. 30")
    secs = 5 #mins * 60
    backups = 1
    start = datetime.now()
    while True:
        print(f"{backups} since {start}")
        backups += 1
        sleep(secs)
        request = get(url)
        open(f"{datetime.now()}.pptx", "wb").write(request.content)

else:
    print("Getting page failed, please restart and enter the correct id.")
