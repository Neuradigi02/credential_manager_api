import asyncio
import glob
import os
import aiofiles
import httpx
import orjson
from requests.auth import HTTPBasicAuth
from src.core.load_config import config
from src.core.logger import logger


async def compile_email_formats_mjml():
    """ Compiles all MJML email templates asynchronously """
    if not config['CompileMails']:
        return {"success": False, "message": "Email compilation is disabled in config"}

    await delete_precompiled_templates()  # Ensures old templates are deleted

    try:
        dir_list = await asyncio.to_thread(os.listdir, 'templates/email/mjml/')  # Non-blocking file listing
        tasks = []

        async with httpx.AsyncClient() as client:
            for file_name_with_extension in dir_list:
                if file_name_with_extension.endswith(".mjml"):
                    tasks.append(process_mjml_file(client, file_name_with_extension))

            await asyncio.gather(*tasks)  # Process all MJML files concurrently

        return {"success": True, "message": "MJML templates compiled successfully"}

    except Exception as e:
        return {"success": False, "message": f"Unexpected error: {str(e)}"}


async def process_mjml_file(client, file_name_with_extension):
    """ Reads MJML template, compiles it using MJML API, and saves it asynchronously """
    file_name = os.path.splitext(file_name_with_extension)[0]
    mjml_path = f'templates/email/mjml/{file_name_with_extension}'
    compiled_path = f'templates/email/compiled/{file_name}.html'

    try:
        async with aiofiles.open(mjml_path, 'r', encoding="utf-8") as file:
            template = await file.read()  # Async file read

        response = await client.post(
            url='https://api.mjml.io/v1/render',
            auth=HTTPBasicAuth(config["mjml"]["AppId"], config["mjml"]["SecretKey"]),
            json={"mjml": template},
            timeout=10
        )
        response.raise_for_status()

        html_content = orjson.loads(response.content).get('html', '')

        async with aiofiles.open(compiled_path, 'w', encoding="utf-8") as file:
            await file.write(html_content)  # Async file write

    except httpx.HTTPStatusError as e:
        logger.error(f"API error: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        logger.error(f"Network error: {str(e)}")
    except orjson.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error processing {file_name_with_extension}: {str(e)}")


async def delete_precompiled_templates():
    """ Deletes all precompiled HTML templates asynchronously """
    try:
        files = await asyncio.to_thread(glob.glob, 'templates/email/compiled/*.html')  # Non-blocking file listing
        await asyncio.gather(*(asyncio.to_thread(os.remove, f) for f in files)) 

    except Exception as e:
        logger.error(f"Error deleting precompiled templates: {str(e)}")
