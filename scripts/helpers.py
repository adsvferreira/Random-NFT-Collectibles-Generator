from brownie import accounts, network, config, Contract, MockV3Aggregator, VRFCoordinatorMock, LinkToken

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-forked"]
DECIMALS = 8
STARTING_ETH_USD_PRICE = 2000
NEWTRINO_TYPE_MAPPING = {0: "MOON", 1: "MEDITATIVE", 2: "PROUD"}
NEWTRINO_TRAITS_MAPPING = {
    "MOON": {"motivation": 100, "loyalty": 70, "patience": 30},
    "MEDITATIVE": {"motivation": 50, "loyalty": 70, "patience": 100},
    "PROUD": {"motivation": 70, "loyalty": 80, "patience": 70},
}

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_account(index: int = None, id: str = None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)  # Ex: af_test_account
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS + FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name: str):
    """Will grab the contract addresses from the brownie config if defined, otherwise, it will deploy a mock version of that contract (if not deployed yet) and return it

    Args:
    contract_name (string)

    Returns:
        brownie.network.contract.ProjectContract: The most recently deployed version of this contract
    """
    print(f"the active network is {network.show_active()}")
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_ETH_USD_PRICE):
    account = get_account()
    print("Deploying Mocks...")
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Mocks Deployed!")


def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):  # 0.1 LINK
    account = account or get_account()
    link_token = link_token or get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # Or using LINK Token interface:
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Contract Funded!")
    return tx


def get_newtrino_type(newtrino_number: int):
    return NEWTRINO_TYPE_MAPPING[newtrino_number]


def get_newtrino_traits(newtrino_number: int):
    newtrino_type = NEWTRINO_TYPE_MAPPING[newtrino_number]
    return NEWTRINO_TRAITS_MAPPING[newtrino_type]
