// An NFT Contract where the token URI can be 1 of 3 possibilities

// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum NewtrinoType {
        MOON,
        MEDITATIVE,
        PROUD
    }
    mapping(uint256 => NewtrinoType) public tokenIdToNewtrinoType;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    // The indexed parameters for logged events will allow you to search for these events using the indexed parameters as filters.
    event typeAssigned(uint256 indexed tokenId, NewtrinoType newtrinoType);

    constructor(
        address _VRFCoordinator,
        address _link_token,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_VRFCoordinator, _link_token)
        ERC721("Newtrinos", "NEWT")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    // Called by VRFCoordinator
    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        NewtrinoType newtrinoType = NewtrinoType(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToNewtrinoType[newTokenId] = newtrinoType;
        emit typeAssigned(newTokenId, newtrinoType);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        // TODO: set token URI inside this function in order to have it in 1 tx;
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner no approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
