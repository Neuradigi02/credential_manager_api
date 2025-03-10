import base64
import aiofiles
import os
from datetime import datetime
from decimal import Decimal
from mimetypes import guess_extension
from dateutil import parser as date_parser
from fastapi import Request
import magic
import pandas as pd
import pdfkit
import pyotp
from src.constants.messages import INVALID_FILE_TYPE
from src.utilities.thread_pool import run_in_threadpool
import platform


async def read_file_async(file_path: str):
    """ Asynchronous file reading """
    async with aiofiles.open(file_path, 'r', encoding="utf-8") as file:
        return await file.read()


def data_frame_to_dict(df: pd.DataFrame):
    return df.to_dict(orient='records')


def hide_mobile_no(mobile_no):
    return (mobile_no[0:2]+'X'*(len(mobile_no)-5)) + mobile_no[len(mobile_no)-3:]


def hide_email_address(email_id):
    return (email_id[0:2]+'X'*(len(email_id.split('@')[0])-4)) + email_id[len(email_id)-(3+len(email_id.split('@')[1])):]


def is_valid_google_authenticator_code(key:str, code:str):
    totp = pyotp.TOTP(key)
    return totp.verify(code)


def generate_google_authenticator_secret_key():
    return pyotp.random_base32()


def intersection(lst1, lst2):
    return set(lst1).intersection(lst2)


def getPdfKitConfig():
    # if not config['IsDevelopment']:
    if platform.system().lower() == "linux":
        return pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    return None


def html_to_pdf_bytes(html):
    pdfKit_config = getPdfKitConfig()
    pdf_bytes = pdfkit.from_string(html, False, configuration=pdfKit_config)
    return pdf_bytes


def get_real_client_ip(request: Request):
    return (
        request.headers.get("X-Real-IP") or
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or
        (request.client.host if request.client else "Unknown")
    )


async def html_to_pdf_bytes_async(html: str):
    """
    Asynchronous wrapper for `html_to_pdf_bytes()` to avoid blocking.
    """
    return await run_in_threadpool(html_to_pdf_bytes, html)


def convert_timestamp_to_datetime_with_timezone(timestamp, desired_timezone, datetime_format):
    """
    Convert a Pandas timestamp or numeric timestamp to a datetime string with a specified timezone.

    Args:
        timestamp: Input timestamp, which can be a Pandas timestamp or a numeric timestamp.
        desired_timezone: The desired timezone for the output string.
        datetime_format: The datetime format of the output string.
    Returns:
        A formatted datetime string with the specified timezone.
    """

    if isinstance(timestamp, (pd.Timestamp, pd.DatetimeIndex)):
        # If input is a Pandas timestamp, convert it to the desired timezone
        timestamp_with_timezone = timestamp.tz_convert(desired_timezone)
    elif isinstance(timestamp, (int, float)):
        # If input is a numeric timestamp, convert it to a Pandas timestamp
        timestamp_with_timezone = pd.Timestamp.fromtimestamp(timestamp, tz=desired_timezone)
    else:
        raise ValueError(
            "Input value must be a Pandas timestamp, numeric timestamp (seconds since epoch), or a Pandas DatetimeIndex.")

        # Format the timestamp as a datetime string with the specified timezone
    formatted_datetime = timestamp_with_timezone.strftime(datetime_format)

    return formatted_datetime


def save_base64_file(data, upload_file_name='Upload', output_directory="static/images/uploads", allowed_extensions=['.png', '.jpg', '.jpeg']):
    """
    Decode the base64 string, identify the file extension, and save the file to disk.

    Parameters:
    - data: base64 encoded string.
    - upload_purpose: Purpose to upload the file, it is used in file name while saving
    - output_directory: The directory where the file will be saved.

    Returns:
    - The path of the saved file.
    """

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if data.startswith("data:"):
        data = data.split(",")[-1]

    # Decode the base64 data
    decoded_data = base64.b64decode(data)

    # Identify the file extension using magic library
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(decoded_data)
    extension = guess_extension(mime_type)

    if extension in allowed_extensions:

        filename = upload_file_name+'_'+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+extension

        file_path = os.path.join(output_directory, filename)

        # Save the file
        with open(file_path, 'wb') as f:
            f.write(decoded_data)

        return filename, file_path
    else:
        raise ValueError(INVALID_FILE_TYPE)


def amount_in_smallest_unit(amount: Decimal, decimals: int):
    return int(amount * (10 ** decimals))


def amount_from_smallet_unit(amount: Decimal, decimals: int):
    return amount/(10 ** decimals)


def is_integer(text):
    try:
        int(text)
        return True
    except ValueError:
        return False
    

def process_js_datetime(js_datetime):
    if js_datetime != "" and js_datetime is not None:
        return date_parser.parse(js_datetime)
    else:
        return None
    