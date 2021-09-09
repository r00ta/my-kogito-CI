
import sys
import requests
import json 

if __name__ == "__main__":
    latest = requests.get("https://quay.io/api/v1/repository/5733d9e2be6485d52ffa08870cabdee0/event-bridge-all-in-one/tag/").text
    tags = json.loads(latest)["tags"]
    tags = sorted(tags, key = lambda x: x["start_ts"], reverse=True)

    print(tags[0]['name'])

