import time
import pytest
from brownie import network
from scripts.advanced_collectible.deploy import deploy_and_create
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract


def test_can_create_advanced_collectible_integration():
    # deploy the contract
    # create an nft
    # get a random newtrino type back
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for external blockchain testing")
    # Act
    advanced_collectible, creation_tx = deploy_and_create()
    time.sleep(60)
    # Assert
    assert advanced_collectible.tokenCounter() == 1
