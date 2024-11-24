import web3.exceptions
from client import *
import os


BANNER = """
============================================================
  ______               __  __            _        _   
 |  ____|             |  \/  |          | |      | |  
 | |__ _ __ ___  ___  | \  / | __ _ _ __| | _____| |_ 
 |  __| '__/ _ \/ _ \ | |\/| |/ _` | '__| |/ / _ \ __|
 | |  | | |  __/  __/ | |  | | (_| | |  |   <  __/ |_ 
 |_|  |_|  \___|\___| |_|  |_|\__,_|_|  |_|\_\___|\__|
============================================================                                           
"""

BASIC_MENU = """
Choose an option (1-6):
    1. List Auctioned Items
    2. Auction an Item
    3. Auction Multiple Items
    4. Buy Item
    5. Cancel an auction
    6. Speak with Merchant

Your choice: """

MERCHANT_CHARACTER = """
============================================================
  ,   A           {}
 / \, | ,        .--.
|    =|= >      /.--.\
 \ /` | `       |====|
  `   |         |`::`|  
      |     .-;`\..../`;_.-^-._
     /\\/  /  |...::..|`   :   `|
     |:'\ |   /'''::''|   .:.   |
      \ /\;-,/\   ::  |..:::::..|
      |\ <` >  >._::_.| ':::::' |
      | `""`  /   ^^  |   ':'   |
      |       |       \    :    /
      |       |        \   :   / 
      |       |___/\___|`-.:.-`
      |        \_ || _/    `
      |        <_ >< _>
      |        |  ||  |
      |        |  ||  |
      |       _\.:||:./_
      | jgs  /____/\____\

============================================================
"""

MERCHANT_MENU = """
Hello! My name is Joe the Merchant.
What would you like me to help you with?
1. Obtain a free NFT!
2. Buy a Legendary Ticket (Only the bravest are capable...) - Price: 270 BHIL Coins
3. Exit
Your choice: """

STATUS_ERROR = 0
STATUS_SUCCESS = 1

PROMPT_TRIES_CONST = 9 # the amount of prompts a client is given per attempt!


def banner():
    print(BANNER)

def print_menu():
    choice = input(BASIC_MENU)
    try:
        choice = int(choice)
        return choice
    except Exception as e:
        print("[x] Invalid choice!")
        return -1

def list_auctioned_items():
    try:
        items = set(bhfm.functions.read_items_for_sale().call())

        print("")
        for item in items:
            print(f"{item[2]} is selling: NFT ID #{item[0]} for {item[1]} bhil_coins")
        
        return STATUS_SUCCESS
    except Exception:
        print("[X] Something went horribly wrong. please try again")
        return STATUS_ERROR

def auction_item():
    try:
        fee = input("Do you want to pay the minimal fee (Y/n): ")
        
        if fee != 'Y' and fee != 'y' and fee != '':
            fee = input("Choose fee (Minimum 5): ")
            fee = int(fee)
            if fee < 5:
                print("[X] Invalid fee!")
                return STATUS_ERROR
        else:
            fee = 5

        nft_id = input("Choose NFT id: ")
        price = input("Enter NFT auction price: ")

        nft_id = int(nft_id)
        price = int(price)
        bhfm.functions.put_for_sale(nft_id, price, fee).transact()
        return STATUS_SUCCESS
    except Exception as e:
        print("[X] Auctioning item failed")
        return STATUS_ERROR

def auction_multiple_items():
    try:
        fee = input("Do you want to pay the minimal fee (Y/n): ")

        if fee != 'Y' and fee != 'y' and fee != '':
            fee = input("Choose fee (Minimum 5): ")
            fee = int(fee)
            if fee < 5:
                print("[X] Invalid fee!")
                return STATUS_ERROR
        else:
            fee = 5

        price = input("Please choose the price: ")
        try:
            price = int(price)
        except Exception:
            print("[X] Invalid price!")
            return STATUS_ERROR

        ids = []
        idx = 0
        while True:
            curr_id = input("Enter the NFT ID you want to sell (index #{}), X to exit the loop: ".format(idx))
            try:
                curr_id = int(curr_id)
                ids.append(curr_id)
                idx += 1
            except Exception:
                break

        bhfm.functions.put_bundle_for_sale(ids, price, fee).transact()
        return STATUS_SUCCESS

    except Exception as e:
        print("[X] Auctioning multiple items failed")
        return STATUS_ERROR
            

def buy_item():
    try:
        nft_id = input("Enter NFT ID to buy: ")
        nft_id = int(nft_id)

        items = set(bhfm.functions.read_items_for_sale().call())
        for item in items:
            if item[0] != nft_id:
                continue
            buy = input(f"NFT ID #{item[0]} costs {item[1]} bhil_coins, do you accept the deal (Y/n): ")
            if buy == 'Y' or buy == 'y' or buy == '':
                bhfm.functions.buy_item(item[2], item[0]).transact()
            else:
                print("OK, didn't buy item.")
            return STATUS_SUCCESS
    
        print("no such ID for sale")
        return STATUS_ERROR

    except web3.exceptions.ContractLogicError:
        print("Couldn't buy NFT requested")
        return STATUS_ERROR
    
    except Exception:
        print("no such ID for sale")
        return STATUS_ERROR

def cancel_auction():
    nft_id_to_cancel = input("Enter NFT id to cancel: ")
    try:
        nft_id_to_cancel = int(nft_id_to_cancel)
        bhfm.functions.cancel_sale(nft_id_to_cancel).transact()
        print(f"Canceled auction for {nft_id_to_cancel}")
        return STATUS_SUCCESS
    except web3.exceptions.ContractLogwicError:
        print("[X] Cannot cancel for an NFT that is not listed by you already.")
        return STATUS_ERROR
    except Exception as e:
        print("[X] Something went wrong!")
        return STATUS_ERROR

def obtain_free_nft():
    new_nft_id = bhfm.functions.next_free_nft_id().call()
    try:
        bhfm.functions.obtain_free_nft().transact()
        print(f"\nObtained NFT {new_nft_id}, Congrats!")
        return STATUS_SUCCESS
    except Exception as e:
        print("[X] Something went wrong!")
        return STATUS_ERROR

def buy_legendary_ticket():
    try:
        bhfm.functions.buy_legendary_ticket().transact()
        print("$$$ $$$ $$$ CONGRATS YOU'RE A BLUEHAT LEGEND! $$$ $$$ $$$")
        return STATUS_SUCCESS
    except web3.exceptions.ContractLogicError:
        print("[X] Can you really afford this? You can't.")
        return STATUS_ERROR
    except Exception as e:
        print("[X] Something went wrong!")
        return STATUS_ERROR

def print_user_balance():
    try:
        balance = bhfm.functions.ShowBHILCoinBalance().call()
        print()
        print(f"Your Wallet balance is: {balance}")
        print()
    except Exception:
        print("Something went horribly wrong. Try again")

def print_merchant_menu():
    choice = input(MERCHANT_MENU)
    try:
        choice = int(choice)
        return choice
    except Exception as e:
        print("[x] Invalid choice!")
        return -1

def merchant():
    print(MERCHANT_CHARACTER)

    while True:
        choice = print_merchant_menu()
        if choice == 1:
            result = obtain_free_nft()
            if result == STATUS_SUCCESS:
                return result
        elif choice == 2:
            result = buy_legendary_ticket()
            print_user_balance()
            if result == STATUS_SUCCESS:
                return result
        elif choice == 3:
            return STATUS_ERROR
        else:
            continue

def interactive_menu(w3):
    banner()
    prompts_count = PROMPT_TRIES_CONST

    # Allow the client to have up to PROMPT_TRIES_CONST prompts.
    while prompts_count > 0:
        print(f"Amount of prompts left: {prompts_count}")
        print_user_balance()
        choice = print_menu()

        if choice == 1:
            prompts_count -= list_auctioned_items()
        elif choice == 2:
            prompts_count -= auction_item()
        elif choice == 3:
            prompts_count -= auction_multiple_items()
        elif choice == 4:
            prompts_count -= buy_item()
        elif choice == 5:
            prompts_count -= cancel_auction()
        elif choice == 6:
            prompts_count -= merchant()
        else:
            continue

def next_account(w3, next_id):
    print("Your turn is over!")
    os.system("clear")
    input("Press Enter to continue:")
    w3.eth.default_account = w3.eth.accounts[next_id]

def main():
    w3 = initialize_web3()
    next_id = 1
    global bhfm
    bhfm = deploy_contract("BHFM.sol", w3)

    while True:
        bhfm.functions.initialize_new_wallet().transact()
        interactive_menu(w3)
        next_account(w3, next_id)
        next_id += 1

if __name__ == "__main__":
    main()
