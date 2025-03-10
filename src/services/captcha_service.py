from fastapi import Request
import httpx
import orjson
from datetime import datetime, timedelta
from io import BytesIO
import random
import base64
from captcha.image import ImageCaptcha
from src.utilities.aes_util import aes
from src.core.load_config import config
from src.utilities.utils import get_real_client_ip


def generate_captcha_text(length=5):
    characters = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return ''.join(random.choice(characters) for i in range(length))


def generate_captcha():
    captcha = ImageCaptcha()
    captcha_text = generate_captcha_text()
    buffer = BytesIO()
    captcha.write(captcha_text, buffer)
    buffer.seek(0)

    # Encode the image to Base64
    base64_image = base64.b64encode(buffer.read()).decode("utf-8")

    expire = datetime.utcnow() + timedelta(minutes=1)
    data = {
        "captcha_text": captcha_text,
        "expiry": expire.timestamp()
    }
    # encrypted_data = aes.encrypt(json.dumps(data))
    encrypted_data = aes.encrypt(orjson.dumps(data).decode())
    return "data:image/png;base64,"+base64_image, encrypted_data


def verify_captcha(encrypted_captcha_text: str, captcha_reponse: str):
    decrypted_obj = orjson.loads(aes.decrypt(encrypted_captcha_text))
    captcha_text = decrypted_obj["captcha_text"]
    expiry = decrypted_obj["expiry"]

    if captcha_text != captcha_reponse:
        return False, "Invalid captcha response!"

    elif float(expiry) < datetime.utcnow().timestamp():
        return False, "Captcha expired!"

    return True, "Captcha valid!"


async def verify_recaptcha_v3(response_token: str, action: str, request: Request):
    
    remoteip = get_real_client_ip(request)

    url = "https://www.google.com/recaptcha/api/siteverify"

    payload = {
        "secret": config["Recaptcha"]["SecretKey"],
        "response": response_token,
        "remoteip": remoteip
    }

    async with httpx.AsyncClient() as client:
        try:
            google_response = await client.post(url, data=payload, timeout=5)
            result = google_response.json()

            # Handle API response
            if not result.get("success"):
                return {"success": False, "message": "Invalid reCAPTCHA token!"}

            if action and result.get("action") != action:
                return {"success": False, "message": "Invalid reCAPTCHA action!"}

            # Score-based validation (Google recommends 0.5 as the threshold)
            score = result.get("score", 0)
            if score < 0.5:
                return {"success": False, "message": "Low reCAPTCHA score. Verification failed."}

            return {"success": True, "message": "reCAPTCHA verified successfully!", "score": score, "action": result.get("action")}

        except httpx.RequestError as e:
            return {"success": False, "message": f"Error contacting reCAPTCHA API: {e}"}
        