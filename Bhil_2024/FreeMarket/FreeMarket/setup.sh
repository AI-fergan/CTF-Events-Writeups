#!/bin/sh

pip install py-solc-x
pip install web3
python3 -c "import solcx; solcx.install_solc('0.8.0')"
npm install -g ganache-cli