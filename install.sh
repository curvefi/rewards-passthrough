python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install eth-ape'[recommended-plugins]'
pip install ape-vyper==0.8.8
ape plugins install arbitrum
ape test