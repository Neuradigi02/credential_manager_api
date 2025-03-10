from fastapi import APIRouter
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.utilities.company_util import company_details, company_datasets
from src.utilities.utils import data_frame_to_dict
from src.core.load_config import arbitrage_trade_config, dapp_config, erc20_token_contract_abi, arbitrage_contract_abi, dapp_contract_abi


router = APIRouter(prefix="/company", tags=["Company"])


@router.get('/details')
def get_details():
    dataset = company_details.to_dict()

    arbitrage_contract_address = arbitrage_trade_config['ContractAddress']
    dapp_contract_address = dapp_config['ContractAddress']
    payment_token_contract_address = dapp_config['PaymentTokenContractAddress']

    if dataset:
        return {
            'success': True, 
            'message': OK, 
            'data': dataset, 
            'user_wallets': data_frame_to_dict(company_datasets['rs_user_wallets']),
            'franchise_wallets': data_frame_to_dict(company_datasets['rs_franchise_wallets']),
            'incomes_list': data_frame_to_dict(company_datasets['rs_incomes']),
            'packages': data_frame_to_dict(company_datasets['rs_packages']),
            'erc20_token_contract_abi': erc20_token_contract_abi,
            'arbitrage_contract_abi': arbitrage_contract_abi,
            'arbitrage_contract_address': arbitrage_contract_address,
            'dapp_contract_abi': dapp_contract_abi,
            'dapp_contract_address': dapp_contract_address,
            'payment_token_contract_address': payment_token_contract_address
            }
        
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
