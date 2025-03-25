from datetime import date
from src.core.db import execute_query


def get_company_details_dict():
    today_date = date.today()
    
    return {
            'company_name': company_details.loc["name"],
            'company_address': company_details.loc["address"],
            'logo': company_details.loc["logo"],
            'website_url': company_details.loc["website"],
            'year': today_date.year,
            'otp_validity_minutes': company_details.loc["otp_validity_minutes"],
            'round_off_digits': company_details.loc["round_off_digits"],
            'company_email': company_details.loc["email"],
            'company_mobile': company_details.loc["mobile"]
            }

company_datasets = execute_query("call usp_get_company_details()")
company_details = company_datasets['rs_company_details'].iloc[0]
company_dict = get_company_details_dict()
