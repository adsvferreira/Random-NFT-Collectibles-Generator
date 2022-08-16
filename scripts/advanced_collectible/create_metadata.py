import os
import json
import requests
from pathlib import Path
from brownie import AdvancedCollectible, network
from metadata.sample_metadata import metadadata_template
from scripts.helpers import get_newtrino_type, get_newtrino_traits

NEWTRINO_TYPE_TO_IMAGE_URI = {
    "PROUD": "https://ipfs.io/ipfs/QmUERHkR3RCUQQXDoEKXzYAHRxSjws5RoDiPMk2ot9yQYj?filename=3-PROUD.json",
    "MOON": "https://ipfs.io/ipfs/QmPCetGnnddwoFWcxwxufLsrFDXHw5Ji1XQ3oFZapsp7oo?filename=2-MOON.json",
    "MEDITATIVE": "https://ipfs.io/ipfs/QmTvzjrLnsVdX6YDDDUNgt3xjmnP7TuMnrLg3QPD7vigzQ?filename=4-MEDITATIVE.json",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        newtrino_type_number = advanced_collectible.tokenIdToNewtrinoType(token_id)
        newtrino_type = get_newtrino_type(newtrino_type_number)
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{newtrino_type}.json"
        collectible_metadata = metadadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating metadata file: {metadata_file_name}")
            collectible_metadata["name"] = newtrino_type
            collectible_metadata["description"] = f"A fuckin' awesome {newtrino_type.capitalize()} Newtrino!"
            collectible_metadata["attributes"] = get_newtrino_traits(newtrino_type_number)
            print(collectible_metadata)
            image_file_path = f"./img/{newtrino_type.lower()}.png"
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = image_uri if image_uri else newtrino_type_to_image_uri[newtrino_type]
            # image_uri = upload_to_ipfs_and_get_uri(image_file_path)
            image_uri = upload_to_pinata_and_get_uri(image_file_path)
            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_pinata_and_get_uri(metadata_file_name)


def upload_to_ipfs_and_get_uri(filepath):
    # rb => binary
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"  # local node
        endpoint = "/api/v0/add"
        url = ipfs_url + endpoint
        res = requests.post(url, files={"file": image_binary})
        ipfs_hash = res.json()["Hash"]
        filename = filepath.split("/")[-1]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri


def upload_to_pinata_and_get_uri(filepath):
    # rb => binary
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        pinata_url = "https://api.pinata.cloud"
        endpoint = "/pinning/pinFileToIPFS"
        url = pinata_url + endpoint
        filename = filepath.split("/")[-1]
        headers = {
            "pinata_api_key": os.getenv("PINATA_API_KEY"),
            "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
        }
        res = requests.post(url, files={"file": (filename, image_binary)}, headers=headers)
        ipfs_hash = res.json()["IpfsHash"]
        file_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(file_uri)
        return file_uri
