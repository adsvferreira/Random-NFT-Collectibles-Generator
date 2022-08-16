from brownie import network, AdvancedCollectible
from scripts.helpers import get_newtrino_type, get_account, OPENSEA_URL
from scripts.advanced_collectible.create_metadata import NEWTRINO_TYPE_TO_IMAGE_URI


# https://ipfs.io/ipfs/QmTvzjrLnsVdX6YDDDUNgt3xjmnP7TuMnrLg3QPD7vigzQ?filename=0-MEDITATIVE.json
# https://ipfs.io/ipfs/QmPCetGnnddwoFWcxwxufLsrFDXHw5Ji1XQ3oFZapsp7oo?filename=1-MOON.json
# https://ipfs.io/ipfs/QmPCetGnnddwoFWcxwxufLsrFDXHw5Ji1XQ3oFZapsp7oo?filename=2-MOON.json
# https://ipfs.io/ipfs/QmUERHkR3RCUQQXDoEKXzYAHRxSjws5RoDiPMk2ot9yQYj?filename=3-PROUD.json
# https://ipfs.io/ipfs/QmTvzjrLnsVdX6YDDDUNgt3xjmnP7TuMnrLg3QPD7vigzQ?filename=4-MEDITATIVE.json


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_advanced_collectibles} tokrnIds")
    for token_id in range(number_of_advanced_collectibles):
        newtrino_type = get_newtrino_type(advanced_collectible.tokenIdToNewtrinoType(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("http://"):
            print("Setting tokenURI of {token_id}")
            set_tokenURI(token_id, advanced_collectible, NEWTRINO_TYPE_TO_IMAGE_URI[newtrino_type])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}")
    print("Please wait up to 20 min and click refresh button")


"""
Final output: https://testnets.opensea.io/collection/newtrinos-v3
"""
