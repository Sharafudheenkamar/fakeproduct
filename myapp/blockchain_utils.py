import json
from web3 import Web3
from web3.datastructures import AttributeDict
from hexbytes import HexBytes
from django.conf import settings

def convert_to_serializable(obj):
    if isinstance(obj, AttributeDict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, HexBytes):
        return obj.hex()
    elif isinstance(obj, list):
        return [convert_to_serializable(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    else:
        return obj


# Initialize web3 connection
web3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER))
web3.eth.default_account = web3.eth.accounts[0]  # Use the first account in Ganache

def load_abi(file_path):
    with open(file_path, 'r') as file:
        contract_data = json.load(file)
        return contract_data['abi']

# Load ABIs
register_company_abi = load_abi("/home/sharafu/Desktop/djangoprojects/djan_maj/Block_chain/product-company-registry/build/contracts/CompanyRegistry.json")
add_product_abi = load_abi("/home/sharafu/Desktop/djangoprojects/djan_maj/Block_chain/product-company-registry/build/contracts/ProductRegistry.json")

# Contract addresses
register_company_contract_address = "0xeF170D8a8c34CFb3A465B64d950caB3324699690"
add_product_contract_address = "0xf0F6D8ef910F71370498993EEbF615a5704FFa97"

# Initialize contracts
register_company_contract = web3.eth.contract(address=register_company_contract_address, abi=register_company_abi)
add_product_contract = web3.eth.contract(address=add_product_contract_address, abi=add_product_abi)

def get_company_details(company_id):
    details = register_company_contract.functions.getCompanyDetails(company_id).call()
    return dict(details) if isinstance(details, tuple) else details

def get_total_companies():
    return register_company_contract.functions.companyCount().call()

def register_company(company_id,company_name, company_email,company_phoneno, owner_address):
    print("hello")
    tx_hash = register_company_contract.functions.registerCompany(company_id,company_name, company_email,company_phoneno, owner_address).transact({
        'from': web3.eth.default_account
    })
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Convert receipt to a serializable format
    receipt_serializable = convert_to_serializable(receipt)
    return receipt_serializable
def edit_company(company_id,company_name,company_email,company_phoneno, owner_address):
    """
    Edit the details of an existing company.
    """
    try:
        print("Editing company...")
        # Call the smart contract function to update the company details
        tx_hash = register_company_contract.functions.editCompany(
            company_id,company_name,company_email,company_phoneno, owner_address
        ).transact({'from': web3.eth.default_account})
        
        # Wait for the transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Convert receipt to a serializable format
        receipt_serializable = convert_to_serializable(receipt)
        return receipt_serializable
    except Exception as e:
        print(f"Error while editing company: {str(e)}")
        raise e


def delete_company(company_id):
    """
    Delete a company by its ID.
    """
    try:
        print("Deleting company...")
        # Call the smart contract function to delete the company
        tx_hash = register_company_contract.functions.deleteCompany(company_id).transact({
            'from': web3.eth.default_account
        })
        
        # Wait for the transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Convert receipt to a serializable format
        receipt_serializable = convert_to_serializable(receipt)
        return receipt_serializable
    except Exception as e:
        print(f"Error while deleting company: {str(e)}")
        raise e


def add_product(product_id, company_id, product_name):
    tx_hash = add_product_contract.functions.addProduct(product_id, company_id, product_name).transact({
        'from': web3.eth.default_account
    })
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return dict(receipt) if isinstance(receipt, dict) else receipt

def edit_product(product_id, company_id, new_product_name):
    """
    Edit the details of an existing product.
    """
    try:
        print("Editing product...")
        # Call the smart contract function to update the product details
        tx_hash = add_product_contract.functions.editProduct(
            product_id, company_id, new_product_name
        ).transact({'from': web3.eth.default_account})

        # Wait for the transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Return the receipt in a serializable format
        return dict(receipt) if isinstance(receipt, dict) else receipt
    except Exception as e:
        print(f"Error while editing product: {str(e)}")
        raise e
def delete_product(product_id):
    """
    Delete a product by its ID.
    """
    try:
        print("Deleting product...")
        # Call the smart contract function to delete the product
        tx_hash = add_product_contract.functions.deleteProduct(product_id).transact({
            'from': web3.eth.default_account
        })

        # Wait for the transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Return the receipt in a serializable format
        return dict(receipt) if isinstance(receipt, dict) else receipt
    except Exception as e:
        print(f"Error while deleting product: {str(e)}")
        raise e

