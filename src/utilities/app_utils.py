
import asyncio
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import orjson
import os
import aiosmtplib
import ipinfo
import orjson
import pandas as pd
import pystache
from src.core.logger import log_async, logger
from src.data_access import misc as misc_data_access
from src.utilities.company_util import company_details, company_dict
from src.core.load_config import config
from src.core.db import log_error
from src.utilities.utils import convert_timestamp_to_datetime_with_timezone, read_file_async


def addCurrencySymbol(amount):
    return company_details['currency_symbol']+str(amount) if company_details['is_currency_symbol_prefixed'] else str(amount)+' '+company_details['currency_symbol']


def convert_timestamp_to_datetime(timestamp):
    return convert_timestamp_to_datetime_with_timezone(timestamp=timestamp, desired_timezone=config["TimeZone"], datetime_format=config["DateTimeLongFormat"])


async def get_ip_info(ip_address: str):
    try:
        ip_details = []
        if not config['IsDevelopment'] and ip_address:
            for ip in ip_address.split(','):
                handler = ipinfo.getHandler(config["IP_Info_Key"])
                details = handler.getDetails(ip.strip())
                ip_details.append(details.details)
        return orjson.dumps(ip_details).decode('utf-8')
    except Exception as e:
        await log_error(e, extra_info='Utils: get_ip_info', extra_data='ip_address: '+ip_address)
        return None


async def get_email_template(template_name):
    return await read_file_async('templates/email/compiled/'+template_name+'.html')
    

async def render_html_template_async(template: str, context: dict, use_company_dict: bool = True):
    """ Offloads pystache rendering to a background thread """
    if use_company_dict:
        context |= company_dict
    return await asyncio.to_thread(pystache.render, template, context)


sms_templates_cache = {}  # Caching templates to avoid repeated file reads


def load_sms_templates():
    global sms_templates_cache
    df = pd.read_csv('templates/sms_templates.csv', delimiter=';', dtype=str)
    df.set_index('template_name', inplace=True)
    sms_templates_cache = df.to_dict(orient="index")


async def get_sms_template(template_name: str, context: dict, use_company_dict: bool = True):
    """ Fetches an SMS template from cache (loads if missing). """
    global sms_templates_cache
    if not sms_templates_cache:
        await asyncio.to_thread(load_sms_templates)

    template_data = sms_templates_cache.get(template_name)
    if not template_data:
        raise ValueError(f"SMS template '{template_name}' not found!")
    
    message = template_data["template_text"]
    if use_company_dict:
        context |= company_dict

    message.format_map(context)

    return template_data["template_id"], message
    

async def send_sms(mobile_no, message, template_id):
    is_sms_system = bool(company_details.loc["is_sms_configured"])
    
    if is_sms_system:
        if mobile_no is not None:
            smsUser = config["SMS"]["User"]
            smsPassword = config["SMS"]["Password"]
            smsSenderId = config["SMS"]["SenderId"]
            
            SMSURL = f"""http://whybulksms.in/app/smsapi/index.php?username={smsUser}
            &password={smsPassword}&campaign=10525&routeid=6&type=text&contacts={mobile_no}
            &senderid={smsSenderId}&msg={message}&template_id={template_id}"""
            
            # response = requests.get(SMSURL)
            
            d = "" #response.text
            
            if(d.find('NOT') == -1):
                return True, "SMS sent successfully!"
            return False, "Failed to send SMS!"
        return False, "Receiver mobile number not found!"
            
    return False, "SMS system not supported!"
  

async def send_mail_async(recipients, subject, mailBody, attachments=None, in_memory_files=None):
    """
    Send an email asynchronously, with or without attachments.

    :param from_email: Sender email address.
    :param from_password: Sender email password.
    :param to_email: Receiver email address.
    :param subject: Email subject.
    :param body: Email body content.
    :param attachments: List of file paths to attach, default is None.
    :param in_memory_files: List of tuples where each tuple is (filename, bytes), default is None.
    """
    
    is_email_system = company_details.loc["is_email_configured"]
    
    if is_email_system:
        if recipients is not None and recipients!= "":
            try:
                emailUser = config["EMAIL"]["User"]
                emailPassword = config["EMAIL"]["AppPassword"]
                emailHostAddress = config["EMAIL"]["HostAddress"]
                emailServerPort = config["EMAIL"]["Port"]
                
                recipients = recipients if isinstance(recipients, list) else [recipients]
            
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = str(company_dict['company_name'])+" <"+emailUser+'>'
                msg['To'] = ", ".join(recipients)

                part = MIMEText(mailBody, 'html')
                msg.attach(part)
            
                # Attach files from file paths if provided
                if attachments:
                    for file_path in attachments:
                        with open(file_path, 'rb') as attachment_file:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment_file.read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', f"attachment; filename= {file_path.split('/')[-1]}")
                            msg.attach(part)

                # Attach in-memory files if provided
                if in_memory_files:
                    for filename, file_bytes in in_memory_files:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(file_bytes)
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
                        msg.attach(part)

                server = aiosmtplib.SMTP(hostname=emailHostAddress, port=emailServerPort)
                await server.connect()
                # await server.starttls()
                # await server.ehlo()
                await server.login(emailUser, emailPassword)
                await server.send_message(msg, sender=emailUser, recipients=recipients)
                await server.quit()
                await log_async(logger.warning, "Email sent successfully!")
                return True, "Email sent successfully!"
                
            except Exception as e:
                await log_async(logger.error, "Unable to send email!"+e.__str__())
            return False, "Unable to send email"

        await log_async(logger.error, "Receiver email not found!")
        return False, "Receiver email not found!"

    await log_async(logger.error, "Email system not supported!")
    return False, "Email system not supported!"


async def generate_routes_json():
    if config["GenerateRoutesJSON"]:
        dataset = await misc_data_access.get_all_routes()

        if len(dataset) > 0:
            df = dataset['rs']

            if len(df) > 0:
                d = df.to_dict(orient='records')

                mod_d = dict({})
                for obj in d:
                    mod_d[obj['control_id']] = obj

                mod_d = orjson.dumps(mod_d).decode("utf-8")

                file_path = config["RoutesJsonFilePaths"]["App"]
                if os.path.exists(file_path):
                    os.remove(file_path)

                with open(file_path, 'a') as file:
                    file.write(mod_d)

                file_path = config["RoutesJsonFilePaths"]["Api"]
                if os.path.exists(file_path):
                    os.remove(file_path)

                with open(file_path, 'a') as file:
                    file.write(mod_d)
    

def get_route_by_control_id(control_id: str):
    file_path = config["RoutesJsonFilePaths"]["Api"]
    with open(file_path, 'r') as file:
        routes = orjson.loads(file.read())
        return routes[control_id]

