import web3
from eth_account import Account
import secrets
from solcx import compile_source

URL = 'HTTP://127.0.0.1:8545'

erc721_set_approval_for_all = [
    {
        "constant": False,
        "inputs": [
            {
                "name": "_operator",
                "type": "address"
            },
            {
                "name": "_approved",
                "type": "bool"
            }
        ],
        "name": "setApprovalForAll",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

erc20_approve = [
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

LEET_AMOUNT = 133713371337

def deploy_contract(contract_filename, w3):
    compiled_sol = compile_source(open(contract_filename, 'r').read(), output_values=['abi', 'bin'], solc_version='0.8.0')
    fm_contract_interface = compiled_sol['<stdin>:BHMarketplace']
    coin_contract_interface = compiled_sol['<stdin>:BHIL_Coin']
    nft_contract_interface = compiled_sol['<stdin>:BHIL_NFT']

    bytecode = fm_contract_interface['bin']
    abi = fm_contract_interface['abi']

    w3.eth.default_account = w3.eth.accounts[0]
    bhfm_to_deploy = w3.eth.contract(abi=abi, bytecode=bytecode)
    gas_estimate = bhfm_to_deploy.constructor().estimate_gas()
    nonce = w3.eth.get_transaction_count(w3.eth.default_account)

    transaction = {
        'from': w3.eth.default_account,
        'gas': gas_estimate,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    }

    tx_hash = bhfm_to_deploy.constructor().transact(transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    bhfm = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

    for acct in w3.eth.accounts:
        w3.eth.default_account = acct

        bhil_collection = w3.eth.contract(address=bhfm.functions.bhil_collection().call(), abi=erc721_set_approval_for_all)
        bhil_collection.functions.setApprovalForAll(bhfm.functions.address, True).transact()

        bhil_coin = w3.eth.contract(address=bhfm.functions.bhil_coin().call(), abi=erc20_approve)
        bhil_coin.functions.approve(bhfm.functions.address, LEET_AMOUNT).transact()

    return bhfm 

def initialize_web3():
    w3 = web3.Web3(web3.Web3.HTTPProvider(URL))
    return w3

def main():
    w3 = initialize_web3()
    deploy_contract("BHFM.sol", w3)

if __name__ == '__main__':
    main()
