import pytest
from brownie import network
from scripts.advanced_collectible.deploy import deploy_and_create
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract


def test_can_create_advanced_collectible():
    # deploy the contract
    # create an nft
    # get a random newtrino type back
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    # Act
    advanced_collectible, creation_tx = deploy_and_create()
    request_id = creation_tx.events["requestedCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, random_number, advanced_collectible.address, {"from": get_account()}
    )
    # Assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToNewtrinoType(0) == random_number % 3
