
from fastapi import APIRouter

from src.utilities.aes_util import aes

router = APIRouter(
    prefix="/encryption",
    tags=["Encryption"]
)


@router.get('/encrypt')
def encrypt(text: str):
    return aes.encrypt(text)


@router.get('/decrypt')
def decrypt(text: str):
    return aes.decrypt(text)
