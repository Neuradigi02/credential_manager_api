from typing import Annotated
from fastapi import Query

REQUIRED                    = Query()
DEFAULT                     = Query()

LOGIN_ID                    = Query()
TWO_FACTOR_AUTH_REQUEST_ID  = Query()

USER_ID                     = Query(min_length=0, max_length=100)
USER_ID_DAPP                = Query(min_length=0, max_length=100)
USER_TYPE                   = Query(regex=r'^(Admin|User|Franchise)$')
USER_TYPE_ALL               = Query(regex=r'^(All|Admin|User|Franchise)$')
NAME                        = Query(regex=r'^[a-zA-Z]+[a-zA-Z.\s]*$')
NAME_OPTIONAL               = Query(regex=r'^$|^[a-zA-Z]+[a-zA-Z.\s]*$')
PASSWORD                    = Query(min_length=0, max_length=30)
OTP                         = Query(min_length=6, max_length=9, regex=r"^\d+$")

CONTACT_TYPE                = Query(regex="^(Mobile|Email)$")
EMAIL_OR_MOBILE_NUMBER      = Query(regex=r"^([a-zA-Z0-9_][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)|(\d{9,15})$")
EMAIL_ID                    = Query(regex=r"^[a-zA-Z0-9_][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
MOBILE_NO                   = Query(min_length=9, max_length=15, regex=r'^\d{9,15}$')


MARITAL_STATUS              = Query(regex=r'^[SM]$')
GENDER                      = Query(regex=r'^[MF]$')

TITLE                       = Query(regex=r'^(Mr|Ms|Mrs)$')
TWO_FACTOR_AUTH_PURPOSE     = Query(regex=r'^(Login|Toggle2FA|ChangePassword|Withdrawal|AdminContactUpdate|UserContactUpdate)$')
TWO_FACTOR_AUTH_MODE        = Query(regex=r'^(Google_authenticator|Mobile|Email)$')


ACCESS_RIGHTS               = Query(regex=r'^(\d+,?)+$')

TRANSFER_TYPE               = Query(regex=r'^(From|To)$')

STATUS_APPROVED_REJECTED    = Query(regex=r'^(Approved|Rejected)$')
STATUS_ALL                  = Query(regex=r'^(All|Pending|Approved|Rejected)$')

PIN_PRODUCT_DISPATCH_STATUS_UPDATE = Query(regex=r'^(Dispatched|Rejected)$')
PIN_PRODUCT_DISPATCH_STATUS_ALL = Query(regex=r'^(All|Pending|Dispatched|Rejected)$')

CREDIT_DEBIT_ACTION         = Query(regex=r'^(Credit|Debit)$')
CREDIT_DEBIT_ALL_ACTION     = Query(regex=r'^(All|Credit|Debit)$')
SUPPORT_MESSAGES_TYPE       = Query(regex=r'^(Inbox|Outbox)$')


CHART_DURATION              = Query(regex=r'^(Day|Week|Month|6Months|Year|5Years|All)$')
