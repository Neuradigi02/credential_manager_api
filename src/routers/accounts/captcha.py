
from fastapi import APIRouter, Request

from src.services.captcha_service import generate_captcha

router = APIRouter(
    tags=["Captcha"]
)


@router.get('/get_captcha')
def get_captcha():
    image, encrypted_data = generate_captcha()
    return {"captcha_image": image, "captcha_text": encrypted_data}
