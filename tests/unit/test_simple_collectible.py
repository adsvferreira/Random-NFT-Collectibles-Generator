import pytest
from brownie import network
from scripts.simple_collectible.deploy import deploy_and_create
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account


def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    simple_collectible = deploy_and_create()
    assert simple_collectible.ownerOf(0) == get_account()
