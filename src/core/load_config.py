import orjson
import yaml


with open("config.yaml") as yaml_data_file:
    config = yaml.safe_load(yaml_data_file)

crypto_payment_gateway_config = config['CryptoPaymentGateway']
arbitrage_trade_config = config['ArbitrageTrade']
erc_20_config = config['ERC20']
dapp_config =  config['DApp']


with open(erc_20_config['AbiJsonPath']) as f:
    erc20_token_contract_abi = orjson.loads(f.read())

with open(arbitrage_trade_config['AbiJsonPath']) as f:
    arbitrage_contract_abi = orjson.loads(f.read())

with open(dapp_config['AbiJsonPath']) as f:
    dapp_contract_abi = orjson.loads(f.read())

