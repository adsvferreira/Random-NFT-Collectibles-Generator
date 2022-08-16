import os
import requests
from os import listdir
from pathlib import Path
from os.path import isfile, join

img_path = "./img/"

PINATA_BASE_URL = "https://api.pinata.cloud"
endpoint = "/pinning/pinFileToIPFS"
headers = {"pinata_api_key": os.getenv("PINATA_API_KEY"), "pinata_secret_api_key": os.getenv("PINATA_API_SECRET")}


def bulk_upload_to_pinata_and_get_image_uris():
    image_uris = []
    for filename in listdir(img_path):
        if not isfile(join(img_path, filename)):
            continue
        file_path = img_path + filename
        with Path(file_path).open("rb") as fp:
            image_binary = fp.read()
        res = requests.post(PINATA_BASE_URL + endpoint, files={"file": (filename, image_binary)}, headers=headers)
        print(res.json())
        ipfs_hash = res.json()["IpfsHash"]
        image_uris.append(f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}")
    print(image_uris)
    return image_uris


def main():
    bulk_upload_to_pinata_and_get_image_uris()
