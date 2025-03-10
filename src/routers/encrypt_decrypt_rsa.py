from fastapi import APIRouter
from src.utilities.rsa_util import rsa 

router = APIRouter(
    prefix="/rsa",
    tags=["RSA Encryption"]
)


@router.get('/encrypt')
def encrypt(text: str):
    return rsa.encrypt(text)


@router.get('/decrypt')
def decrypt(text: str):
    return rsa.decrypt(text)
