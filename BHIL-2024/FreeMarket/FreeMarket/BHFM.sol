// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "openzeppelin/openzeppelin-contracts-4.0.0/contracts/token/ERC20/ERC20.sol";
import "openzeppelin/openzeppelin-contracts-4.0.0/contracts/token/ERC721/ERC721.sol";

// BHIL Coin Contract
contract BHIL_Coin is ERC20 {
    address admin;

    constructor(string memory name, string memory symbol) ERC20(name, symbol) {
        admin = msg.sender;
    }

    function mint(address to, uint256 amount) public {
        require(msg.sender == admin, "Only the admin can generate money");
        _mint(to, amount);
    }

    function burn(address wallet, uint256 amount) public {
        _burn(wallet, amount);
    }

    function approve(address spender, uint256 amount) public override returns (bool) { 
        _approve(msg.sender, spender, amount);
        return true;
    }
}

// BHIL NFT Contract
contract BHIL_NFT is ERC721 {
    address admin;
    
    constructor(string memory name, string memory symbol) ERC721(name, symbol) {
        admin = msg.sender;
    }

    function mint(address to, uint256 nft_id) public {
        require(msg.sender == admin, "Only the admin can generate NFTs");
        _mint(to, nft_id);
    }
}

// A struct representing a sale offer of an item, from a specific seller
struct SellOffer {
        uint256 nft_id;
        uint256 price;
        address seller; 
}

// A struct representing all items for sale of a specific client
struct ClientAuctions
{
    uint256 fee;     
    mapping(uint256 => SellOffer) offers; // Mapping an nft_id to a SellOffer
    uint256[] ids_for_sale; // ids of all of the NFTs that are for sale
}

contract BHMarketplace
{
    bool public initialized;
    mapping(address => bool) public wallet_is_init;

    mapping(address => ClientAuctions) public all_auctions; // Map an Address of a sender to the their Auctions    
    address[] public sellers; // Saving the keys for all_auctions

    BHIL_NFT public bhil_collection;
    BHIL_Coin public bhil_coin;
    uint256 public next_free_nft_id;

    SellOffer[] public all_offer_list; 

    uint256 public constant MIN_FEE = 1;
    uint256 public constant INITIAL_WALLET_BALANCE = 100;
    uint256 public constant LEGENDARY_PRICE = 270;

    address[] public winners;

    constructor ()
    {
        bhil_coin = new BHIL_Coin{salt: keccak256("BHIL_Coin")}("BHIL Coin", "BHIL_Coin");
        bhil_collection = new BHIL_NFT{salt: keccak256("BHIL_NFT")}("BHIL NFT", "BHIL_NFT");

        next_free_nft_id = 2024;
    }


    /// -----------------------------------------------------------------------------
    ///  HELPER FUNCTIONS
    /// -----------------------------------------------------------------------------

    // Helper functions to allow deleting an item from an array.
    function sellers_delete_by_seller(address _value) public {
        for (uint i = 0; i < sellers.length; i++) {
            if (sellers[i] == _value) {
                // Replace the element to delete with the last element
                sellers[i] = sellers[sellers.length - 1];
                // Remove the last element
                sellers.pop();
                // Exit the loop after deleting the first occurrence of the value
                return;
            }
        }
    }

    // Helper fucnction to allow deleting an NFT from the NFTs-for-sale array.
    function nfts_delete_by_nft_id(address seller, uint256 nft_id) public {
        for (uint i = 0; i < all_auctions[seller].ids_for_sale.length; i++) {
            if (all_auctions[seller].ids_for_sale[i] == nft_id) {
                // Replace the element to delete with the last element
                all_auctions[seller].ids_for_sale[i] = all_auctions[seller].ids_for_sale[all_auctions[seller].ids_for_sale.length - 1];
                // Remove the last element
                all_auctions[seller].ids_for_sale.pop();
                // Exit the loop after deleting the first occurrence of the value
                return;
            }
        }
    }

    // Helper function to read all auctions
    function read_items_for_sale() public returns (SellOffer[] memory) {
        for (uint256 i = 0; i < sellers.length; i++)
        {
            for (uint256 j = 0; j < all_auctions[sellers[i]].ids_for_sale.length; j++)
            {
                uint256 curr_id = all_auctions[sellers[i]].ids_for_sale[j];
                all_offer_list.push(all_auctions[sellers[i]].offers[curr_id]);
            }
        }

        return all_offer_list;
    }


    /// -----------------------------------------------------------------------------
    ///  MARKET PLACE LOGIC
    /// -----------------------------------------------------------------------------

    // This is called implicitly by the client-side, in order to initialize a wallet.
    function initialize_new_wallet() public
    {  
        bhil_coin.mint(msg.sender, INITIAL_WALLET_BALANCE);
    }

    /*  
     * [1]: Selling items:
     * Put an item for sale, given an item_id, the price, and the fee.
     */
    function put_for_sale(uint256 nft_id, uint256 price, uint256 fee) public {
        require(fee >= MIN_FEE, "Auctioning an item costs money!"); // No spamming the market.

        // Record the sell offer by the client.
        all_auctions[msg.sender].fee = fee;
        all_auctions[msg.sender].offers[nft_id] = SellOffer(nft_id, price, msg.sender);
        all_auctions[msg.sender].ids_for_sale.push(nft_id); // Save the ID of the nfts we're selling.

        sellers.push(msg.sender); // Add the seller to the list of all sellers
        
        // Tax the seller, and burn the money.
        safeTransferFromCoin(msg.sender, address(this), fee);

        // Take the item from the seller.
        safeTransferFromItem(msg.sender, address(this), nft_id);
    }

    /*
     * Selling a bundle of items for the same price, why go through the hussle of calling `put_for_sale` 100 times?
     */
    function put_bundle_for_sale(uint256[] calldata nft_ids, uint256 price, uint256 fee) public {
        for (uint256 idx = 0; idx < nft_ids.length; ++idx) {
            put_for_sale(nft_ids[idx], price, fee);
        }
    }

    /*
     * Cancel an auction that was submitted.
     */
    function cancel_sale(uint256 nft_id) public 
    {
        SellOffer memory offer = all_auctions[msg.sender].offers[nft_id];
        uint256 fee_return = all_auctions[msg.sender].fee;
        uint256 delete_idx = 0;

        require(offer.nft_id != 0, "Require a valid NFT");
        require(offer.nft_id == nft_id, "Validate the offer cancelled is for the specified item");

        // Remove the seller from the list of sellers.
        sellers_delete_by_seller(msg.sender);

        // Delete the sale offer that was specified to be canceled.
        delete all_auctions[msg.sender].offers[nft_id];
        nfts_delete_by_nft_id(msg.sender, nft_id);

        // Return the fee to seller.
        bhil_coin.mint(msg.sender, fee_return);
    }


    // Burn a certain amount of BHIL coins to a specific wallet
    function burnBHILCoins(address from, uint256 amount) public {
        bhil_coin.burn(from, amount);
    }

    // Show the BHIL coins balance of a wallet
    function ShowBHILCoinBalance() public view returns (uint256) {
        return bhil_coin.balanceOf(msg.sender);
    }

    
    // Transfer BHIL coins from a sender to a recepient
    function safeTransferFromCoin(address sender, address recipient, uint256 amount) private {
        bool sent = bhil_coin.transferFrom(sender, recipient, amount);
        require(sent, "transferFrom failed");
    }

    // Transfer a BHIL NFT from a sender to a recipient
    function safeTransferFromItem(address sender, address recipient, uint256 item_id) private
    {
        bhil_collection.transferFrom(sender, recipient, item_id);
    }

    /*
     * [3]: Buying items.
     *      Once an item is put for sale, a buyer can buy the item for the price that it was auctioned for.
     */
    function buy_item(address seller, uint256 nft_id) public {
        SellOffer memory offer = all_auctions[seller].offers[nft_id];
        uint256 price = offer.price;
    
        require(offer.nft_id != 0, "Require a valid NFT");
        require(offer.nft_id == nft_id, "Validate the offer cancelled is for the specified item");

        // Remove the item from the Auction House.
        delete all_auctions[seller].offers[nft_id];
        nfts_delete_by_nft_id(seller, nft_id); 

        // Transfer the money from the buyer to the seller
        safeTransferFromCoin(msg.sender, seller, price);

        // Remove the seller from the list of sellers.
        sellers_delete_by_seller(seller);

        // Transfer the NFT from the Marketplace to the buyer.
        safeTransferFromItem(address(this), msg.sender, nft_id);
    }

    /*
    ------------------------------------------------------------------------
        This section is for the Marketplace's NPC Merchant!
        It gives a free NFT upon request.
    ------------------------------------------------------------------------
    */
    function obtain_free_nft() public {
        
        // Create a Free NFT of Type "Blue Gloves".
        // Identified by nft_id 2024 and above.
        bhil_collection.mint(msg.sender, next_free_nft_id);

        // approve the BHMarketplace to transfer the freshly minted nft on behalf of the sender.
        next_free_nft_id++;
    }

    // Only the richest of the richest can become legendary.
    // In order to become legendary, one has to have enough money.
    function buy_legendary_ticket() public {

        // This function will fail & revert if the sender does not have enough money.
        safeTransferFromCoin(msg.sender, address(this), LEGENDARY_PRICE);

        // Add the winner!
        winners.push(msg.sender);
    }
}
