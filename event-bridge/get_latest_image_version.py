
import sys
import requests
import json 

if __name__ == "__main__":
    image_name = sys.argv[1]
    latest = requests.get("https://quay.io/api/v1/repository/5733d9e2be6485d52ffa08870cabdee0/{}/tag/".format(image_name)).text
    tags = json.loads(latest)["tags"]
    tags = sorted(tags, key = lambda x: x["start_ts"], reverse=True)

    print(tags[0]['name'])

