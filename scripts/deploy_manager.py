import os
import click
import time
import sys
from ape import project, Contract

from ape.cli import ConnectedProviderCommand, account_option

from scripts.get_constructor_abi_passthrough import get_constructor_args

# make soure to reload env variables on change
OWNERSHIP_AGENT = os.getenv('OWNERSHIP_AGENT')
PARAMETER_AGENT = os.getenv('PARAMETER_AGENT')
EMERGENCY_AGENT = os.getenv('EMERGENCY_AGENT')
GUARDS = os.getenv('GUARDS')

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
    
    # distributors = ["0x9f499A0B7c14393502207877B17E3748beaCd70B", "0x84bC1fC6204b959470BF8A00d871ff8988a3914A"]
    # rewards_tokens = ["0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000000"]

    reward_receivers = []
    distributors = []
    agents = [OWNERSHIP_AGENT, PARAMETER_AGENT, EMERGENCY_AGENT]

    guards = GUARDS.split(",")
    
    click.echo(reward_receivers)
    click.echo(distributors)
    click.echo(guards)
    click.echo(agents)

    #deploy = account.deploy(project.Passthrough, max_priority_fee="10 wei", max_fee=max_fee, gas_limit="4000000")

    deploy = account.deploy(project.Passthrough, agents, reward_receivers, guards, distributors, max_priority_fee="10 wei", max_fee=max_fee, gas_limit="400000")
    get_constructor_args(agents, reward_receivers, guards, distributors)

cli.add_command(deploy)


@click.command(cls=ConnectedProviderCommand)
@account_option()
@click.option('--dry-run', is_flag=True, help='Run in dry-run mode without making actual deployments')
def deploy_many(ecosystem, network, provider, account, dry_run=False):
    if dry_run:
        print("Dry run mode enabled. No deployments will be made.")
        # Use a dummy account for dry runs
        account = type('DummyAccount', (), {
            'address': '0x0000000000000000000000000000000000000000',
            'deploy': lambda *args, **kwargs: None,
            'set_autosign': lambda x: None
        })()
    else:
        print(f"Using account: {account}")
        account.set_autosign(True)
   
    max_fee, blockexplorer = setup(ecosystem, network)

    # compiler_settings = {'settings': CompilerSettings(evm_version='shanghai', optimize=OptimizationLevel.CODESIZE)}
    reward_receivers = []
    distributors = []
    guards = GUARDS.split(",")
    agents = [OWNERSHIP_AGENT, PARAMETER_AGENT, EMERGENCY_AGENT]

    new_gauge_manager = "0xf7Bd34Dd44B92fB2f9C3D2e31aAAd06570a853A6"

    print(f"Deploying {ecosystem.name} {network.name}")

    with open("contracts/abi/ChildLiquidityGauge.json", "r") as f:
        contract_abi = f.read()

    REWARD_TOKEN = os.getenv('REWARD_TOKEN')
    chainname = ecosystem.name

    if chainname == 'arbitrum':

        gauges = os.getenv('GAUGE_LIST').split(",")
        names = os.getenv('GAUGE_LIST_NAME').split(",")

        
    if chainname == 'optimism':

        # Import lending gauges from env
        GAUGE_LEND_CRV_LONG = os.getenv('GAUGE_LEND_CRV_LONG')
        GAUGE_LEND_OP_LONG = os.getenv('GAUGE_LEND_OP_LONG') 
        GAUGE_LEND_WBTC_LONG = os.getenv('GAUGE_LEND_WBTC_LONG')
        GAUGE_LEND_WETH_LONG = os.getenv('GAUGE_LEND_WETH_LONG')
        GAUGE_LEND_WSTETH_LONG = os.getenv('GAUGE_LEND_WSTETH_LONG')
        GAUGE_TRICRYPTO_CRVUSD = os.getenv('GAUGE_TRICRYPTO_CRVUSD')
        GAUGE_TRICRV = os.getenv('GAUGE_TRICRV')
        GAUGE_WSTETH_ETH = os.getenv('GAUGE_WSTETH_ETH')
        GAUGE_SCRVUSD = os.getenv('GAUGE_SCRVUSD')


        gauges = [GAUGE_LEND_CRV_LONG, GAUGE_LEND_OP_LONG, GAUGE_LEND_WBTC_LONG, GAUGE_LEND_WETH_LONG, GAUGE_LEND_WSTETH_LONG, GAUGE_TRICRYPTO_CRVUSD, GAUGE_TRICRV, GAUGE_WSTETH_ETH, GAUGE_SCRVUSD]
        names = ["LLama Lend CRV Long", "LLama Lend OP Long", "LLama Lend WBTC Long", "LLama Lend WETH Long", "LLama Lend wstETH Long", "crvUSD/WBTC/WETH (Tricrypto-crvUSD)", "crvUSD/CRV/OP (TriCRV-Optimism)", "wstETH/ETH", "crvUSD/scrvUSD"]

        #gauges = [GAUGE_SCRVUSD]
        #names = ["crvUSD/scrvUSD"]

    if chainname == 'taiko':

        GAUGE_USDC_USDT = os.getenv('GAUGE_USDC_USDT')
        GAUGE_CRVUSD_USDT = os.getenv('GAUGE_CRVUSD_USDT')
        GAUGE_CRVUSD_USDC = os.getenv('GAUGE_CRVUSD_USDC')

        gauges = [GAUGE_USDC_USDT, GAUGE_CRVUSD_USDT, GAUGE_CRVUSD_USDC]
        names = ["USDC/USDT", "crvUSD/USDT", "crvUSD/USDC"]

        gauges = [GAUGE_CRVUSD_USDC]
        names = ["crvUSD/USDC"]

        print(gauges)
        print(names)

    if chainname == 'sonic':

        GAUGE_LEND_SCETH_LONG = os.getenv('GAUGE_LEND_SCETH_LONG')
        GAUGE_LEND_SCUSD_LONG = os.getenv('GAUGE_LEND_SCUSD_LONG')
        GAUGE_LEND_STS_LONG = os.getenv('GAUGE_LEND_STS_LONG')
        GAUGE_LEND_WOS_LONG = os.getenv('GAUGE_LEND_WOS_LONG')
        GAUGE_LEND_WS_LONG = os.getenv('GAUGE_LEND_WS_LONG')

        gauges = [GAUGE_LEND_SCETH_LONG, GAUGE_LEND_SCUSD_LONG, GAUGE_LEND_STS_LONG, GAUGE_LEND_WOS_LONG, GAUGE_LEND_WS_LONG]
        names = ["LLama Lend Sonic ETH (scETH)", "LLama Lend Sonic USD (scUSD)", "LLama Lend Beets Staked Sonic (stS)", "LLama Lend wrapped Origin Sonic (wOS)", "LLama Lend wraped sonic (wS)"]
        # remove first 4 gauges
        for i in range(0, 4):
            gauges.pop(0)
            names.pop(0)

    i = 0
    sleep_time = 10

    for reward_receiver in gauges:
        print(f"Deploying {names[i]}")
        if not dry_run:
            passthrough = account.deploy(project.Passthrough, agents, [], guards, [], max_priority_fee="10 wei", max_fee=max_fee, gas_limit="400000")
            get_constructor_args(agents, reward_receivers, guards, distributors)
            time.sleep(sleep_time)
            passthrough.set_name(names[i], sender=account)
        
        print(f"Setting gauge to {gauges[i]}")
        print(f"Setting reward receiver to {reward_receiver}")
        if not dry_run:
            time.sleep(sleep_time)
            passthrough.set_single_reward_receiver(reward_receiver, sender=account)
            time.sleep(sleep_time)
            passthrough.set_single_reward_token(REWARD_TOKEN, sender=account)


        gauge = Contract(reward_receiver, abi=contract_abi)

        manager = gauge.manager()
        print(f"Manager: {manager}")
     
        # Log contract address and transaction info
        with open(f"deployments/deploy_passthrough_contracts_{chainname}.log", "a+") as f:
            if not dry_run:
                passthrough_address  = passthrough.address
            else:
                passthrough_address = "no passthrough address, as this is a dry run"
            f.write(f"Passthrough Contract: {passthrough_address}\n")
            f.write(f"Name: {names[i]}\n")
            f.write(f"Reward Receiver/Gauge: {reward_receiver}\n")
            f.write(f"Reward Token: {REWARD_TOKEN}\n")
            f.write(f"Gauge Manager: {manager}\n")
            f.write(f"Link: {blockexplorer}/address/{passthrough_address}\n")
            f.write("-" * 20 + "\n")
            f.write(f"Done with {names[i]} Passthrough\n")
            f.write("-" * 20 + "\n")

            f.write(f"Set name: set_name('{names[i]}')\n")
            f.write(f"Set reward receiver: set_single_reward_receiver('{reward_receiver}')\n")
            f.write(f"Set single reward token: set_single_reward_token('{REWARD_TOKEN}')\n")

            f.write("-" * 20 + "\n")
            f.write(f"Change this on gauge\n")
            f.write("-" * 20 + "\n")
    
            f.write(f"{blockexplorer}/address/{reward_receiver}#writeContract#F20\n")
            f.write(f"Set reward distributor: set_reward_distributor('{REWARD_TOKEN}', '{passthrough_address}')\n")
            if manager != new_gauge_manager:
                f.write(f"Set manager: set_manager('{new_gauge_manager}') <-- this is mima\n")
            f.write("-" * 80 + "\n\n")

        i += 1
        # Sleep for 1 second between deployments
        if not dry_run:
            time.sleep(sleep_time)

cli.add_command(deploy_many)

def setup(ecosystem, network):

    click.echo(f"ecosystem: {ecosystem.name}")
    click.echo(f"network: {network.name}")

    if ecosystem.name == 'arbitrum':
        max_fee = "0.1 gwei"
        if network.name == 'sepolia':
            blockexplorer = "https://sepolia.arbiscan.io"
        else:
            blockexplorer = "https://arbiscan.io"
    elif ecosystem.name == 'optimism':
        max_fee = "0.0001 gwei"
        blockexplorer = "https://optimistic.etherscan.io"
    elif ecosystem.name == 'taiko':
        if network.name == 'sepolia':   
            max_fee = "0.01 gwei"
            blockexplorer = "https://testnet.sonicscan.org"
        else:
            max_fee = "0.01 gwei"
            blockexplorer = "https://taikoscan.io"

    elif ecosystem.name == 'sonic':
        max_fee = "66 gwei"
        blockexplorer = "https://sonicscan.org/"
    else:
        max_fee = "0.1 gwei"
        blockexplorer = "https://sepolia.arbiscan.io"
    return max_fee, blockexplorer

