import os
import click
import time

from ape import project

from ape.cli import ConnectedProviderCommand, account_option

from scripts.get_constructor_abi_passthrough import get_constructor_args

# GUARDS = os.getenv('GUARDS')
# GUARDS_AND_CAMPAIGNS = os.getenv('GUARDS_AND_CAMPAIGNS')
# REWARD_TOKEN = os.getenv('REWARD_TOKEN')
# RECOVERY_ADDRESS = os.getenv('RECOVERY_ADDRESS')
# EXISTING_TEST_GAUGE = os.getenv('EXISTING_TEST_GAUGE')

# REWARD_TOKEN_TESTNET = os.getenv('REWARD_TOKEN_TESTNET')
# GAUGE_ALLOWLIST = os.getenv('GAUGE_ALLOWLIST')

# DEPLOYED_DISTRIBUTOR = os.getenv('DEPLOYED_DISTRIBUTOR')
# CRVUSD_ADDRESS = os.getenv('CRVUSD_ADDRESS')
# EXECUTE_REWARD_AMOUNT = os.getenv('EXECUTE_REWARD_AMOUNT')

@click.group()
def cli():
    pass

@click.command(cls=ConnectedProviderCommand)
@account_option()
def info(ecosystem, provider, account, network):
    click.echo(f"ecosystem: {ecosystem.name}")
    click.echo(f"network: {network.name}")
    click.echo(f"provider_id: {provider.chain_id}")
    click.echo(f"connected: {provider.is_connected}")
    click.echo(f"account: {account}")

cli.add_command(info)


@click.command(cls=ConnectedProviderCommand)
@account_option()
def deploy(ecosystem, network, provider, account):
    account.set_autosign(True)
   
    max_fee, blockexplorer = setup(ecosystem, network)

    #gauges = GAUGE_ALLOWLIST.split(",")
    #click.echo(gauges)
    
    guards = ["0x0000000000000000000000000000000000000000"]
    distributors = ["0x9f499A0B7c14393502207877B17E3748beaCd70B", "0x84bC1fC6204b959470BF8A00d871ff8988a3914A"]
    rewards_tokens = ["0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000000"]

    reward_receivers = []
    distributors = []
    guards = []
    click.echo(guards)

    deploy = account.deploy(project.Passthrough, reward_receivers, guards, distributors, max_priority_fee="10 wei", max_fee=max_fee, gas_limit="400000")

    get_constructor_args(reward_receivers, guards, distributors)

cli.add_command(deploy)

def setup(ecosystem, network):

    click.echo(f"ecosystem: {ecosystem.name}")
    click.echo(f"network: {network.name}")

    if ecosystem.name == 'arbitrum':
        max_fee = "1 gwei"
        blockexplorer = "https://sepolia.arbiscan.io"
    elif ecosystem.name == 'taiko':
        max_fee = "0.1 gwei"
        blockexplorer = "https://taikoscan.io"
    else:
        max_fee = "0.1 gwei"
        blockexplorer = "https://sepolia.arbiscan.io"
    return max_fee, blockexplorer

