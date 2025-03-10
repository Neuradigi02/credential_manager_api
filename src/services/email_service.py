from src.utilities.app_utils import get_email_template, render_html_template_async, send_mail_async


async def send_joining_mail(user_id, user_name, email_id, joining_amount, sponsor_id, referral_link, in_memory_files=None):
    template = await get_email_template('registration')
    
    context = {
            'user_id':user_id,
            'user_name':user_name,
            'joining_amount':joining_amount,
            'sponsor_id':sponsor_id,
            'referral_link':referral_link
        }

    template = await render_html_template_async(template, context)
    
    return await send_mail_async(email_id, 'Welcome Mail', template, None, in_memory_files=in_memory_files)
            

async def send_reset_password_link_mail(user_id, user_name, email_id, reset_link):
    template = await get_email_template('reset_password')
    
    context = {
            'user_id':user_id,
            'user_name':user_name,
            'reset_link':reset_link
        }

    template = await render_html_template_async(template, context)
                                
    return await send_mail_async(email_id, 'Reset Password', template)


async def send_contact_verification_otp_mail(user_id, user_name, email_id, otp):
    template = await get_email_template('email_verification_otp')
    
    context = {
            'user_id':user_id,
            'user_name':user_name,
            'otp':otp
        }

    template = await render_html_template_async(template, context)
                                
    return await send_mail_async(email_id, 'OTP for Email Verification', template)


async def send_contact_verification_otp_mail_before_registration(email_id, otp):
    template = await get_email_template('email_verification_otp_before_registration')
    
    context = {
            'otp':otp
        }

    template = await render_html_template_async(template, context)
                                
    return await send_mail_async(email_id, 'OTP for Email Verification', template)


async def send_email_verification_link_mail(user_id, user_name, verification_link, email_id):
    template = await get_email_template('email_verification_link')
    
    context = {
            'user_id':user_id,
            'user_name':user_name,
            'verification_link':verification_link
        }
      
    template = await render_html_template_async(template, context)
                                 
    return await send_mail_async(email_id, 'Email Verification Link', template)


async def send_two_factor_auth_otp_mail(user_id, user_name, email_id, otp):
    template = await get_email_template('two_factor_auth_otp')
    
    context = {
            'user_id':user_id,
            'user_name':user_name,
            'otp':otp
        }
      
    template = await render_html_template_async(template, context)
                                
    return await send_mail_async(email_id, 'Two Factor Authentication OTP', template)


async def send_topup_mail(user_id, user_name, email_id, package_name, pin_value, in_memory_files=None):
    template = await get_email_template('topup_successful')
    
    context = {
            'user_id':user_id,
            'user_name':user_name,
            'package_name':package_name,
            'pin_value':pin_value
        }
      
    template = await render_html_template_async(template, context)
                         
    return await send_mail_async(email_id, 'Topup Successful', template, None, in_memory_files=in_memory_files)


async def send_withdrawal_successful_mail(user_id, user_name, email_id, amount):
    template = await get_email_template('withdrawal_successful')
    
    context = {
            'user_id':user_id,
            'user_name':user_name,
            'amount':amount
        }
      
    template = await render_html_template_async(template, context)
                                
    return await send_mail_async(email_id, 'Withdrawal Successful', template)


async def send_withdrawal_rejected_mail(user_id, user_name, email_id, amount):
    template = await get_email_template('withdrawal_rejected')
    
    context = {
            'user_id':user_id,
            'user_name':user_name,
            'amount':amount
        }
      
    template = await render_html_template_async(template, context)
                                
    return await send_mail_async(email_id, 'Withdrawal Rejected', template)
