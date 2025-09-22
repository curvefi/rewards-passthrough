all:

start_env:
	# source will not work, but this is for cmd documentation
	source .env
	source .venv/bin/activate

deploy_info:
	ape run scripts/deploy_manager.py info --network arbitrum:mainnet-fork:foundry

get_constructor_abi:
	python  scripts/get_constructor_abi.py

deploy_arbitrum_sepolia_infura:
	ape run scripts/deploy_manager.py deploy --network arbitrum:sepolia:infura

deploy_arbitrum:
	ape run scripts/deploy_manager.py deploy --network arbitrum:mainnet:node

deploy_arbitrum_sepolia:
	ape run scripts/deploy_manager.py deploy --network arbitrum:sepolia:node

deploy_many_arbitrum:
	ape run scripts/deploy_manager.py deploy-many --network arbitrum:mainnet:node

deploy_many_arbitrum_dry_run:
	ape run scripts/deploy_manager.py deploy-many --network arbitrum:mainnet:node --dry-run


deploy_many_arbitrum_sepolia_dry_run:
	ape run scripts/deploy_manager.py deploy-many --network arbitrum:sepolia:node --dry-run

deploy_info_arbitrum:
	ape run scripts/deploy_manager.py info --network arbitrum:mainnet:node

deploy_taiko:
	ape run scripts/deploy_manager.py deploy --network taiko:mainnet:node


deploy_testnet:
	ape run scripts/deploy_manager.py deploy-many --network ethereum:local:test

filter_log:
	ag --nonumbers "(Name|Link|Passthrough )" deployments/deploy_passthrough_contracts_sonic.log > deployments/deploy_passthrough_contracts_sonic_passthrough_only.log

install:
	uv sync

pre_commit:
	pre-commit run --all-files

import_pvk:
	ape accounts import arbideploy

networks_list:
	ape networks list

noisy_test:
	ape test -rP  --capture=no --network ethereum:local:test

test:
	ape test --network ethereum:local:test
