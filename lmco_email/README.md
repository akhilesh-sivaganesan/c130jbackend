# lmco_email

MX Record aware helper class for email settings and sending of emails based off of [Configure SMTP Settings for outgoing E-mail on Applications](https://docs.us.lmco.com/pages/viewpage.action?spaceKey=ITO&title=Configure+SMTP+Settings+for+outgoing+E-mail+on+Applications).

## Prerequisites

### Steps for making LMCO_Email work with AWS Lambda

#### Note: Execution Role must have Lambda VPC and AWS VPC full access policies

1. Once the function has been created, scroll down to the VPC section.
2. Add the specific VPC settings used within your Team/Project composed of.
    * VPC
    * Subnets
    * Security Groups
3. Once these settings are added to the function, upload the LMCO_Email deployment package with your lambda_function.py to AWS and the outgoing emails should now send.

## Installing

    pip install https://apai.pages.gitlab.us.lmco.com/incubator/lmco_email/lmco_email-latest-py3-none-any.whl

## Getting Started

### Testing

Run `python lmco_email.py` to test functionality. `main()` will prompt you for a sender and recipient email address.

### To use within a script

    # Import module
    from lmco_email import lmco_email

    # Create instance
    emailer=lmco_email.lmco_email(
        sender='firstname.lastname@lmco.com'
        ,recipients=['firstname.lastname@lmco.com']
        ,server='relay-lmi.ems.lmco.com'            # Default defined in __init__ or override with custom value
        ,port=25                                    # Default defined in __init__ or override with custom value
    )

    # Send email without attachment
    emailer.send_mail(
        subject=f'Message subject string.'
        ,message_body=f'Message body text.'
    )

    # Send email with attachment(s)
    # list_of_files_to_attach is a list of pathlib.Path objects or similar
    emailer.send_mail(
        subject=f'Message subject string.'
        ,message_body=f'Message body text.'
        ,files=list_of_files_to_attach
    )
