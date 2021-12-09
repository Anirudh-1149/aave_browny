from brownie import network, interface, config
from brownie.network import web3
from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from brownie import config, network
from web3 import Web3

amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    lending_pool = get_lending_pool()
    print(lending_pool)
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    tx = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited")


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving")
    erc_20 = interface.IERC20(erc20_address)
    tx = erc_20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved")
    return tx


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
