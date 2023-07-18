import os

import smtplib
from smtplib import SMTPResponseException

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import dns.resolver

import logging
_logger=logging.getLogger(__name__)

class lmco_email:
    """Class for email settings and sending of emails on the LMI.
    """

    def __init__(self, sender=None, recipients=None, reply_to=None, server='relay-lmi.ems.lmco.com', port=25):
        """Initialize EmailSettings

        Keyword Arguments:
            sender {str} -- Sender email address. Must be a valid email address. (default: {None})
            recipients {list of str} -- List of recipient email address[es]. (default: {None})
            reply_to {str} -- Reply-To email address. Must be a valid email address. (default: {Sender})
            server {str} -- Server Fully Qualified Domain Name (default: {relay-lmi.ems.lmco.com})
            port {int} -- Server SMTP port (default: {25})
        """

        self.sender=sender
        self.recipients=list(recipients.split(','))
        self.reply_to=reply_to if reply_to is not None else sender
        self.server=str(dns.resolver.query(server, 'MX')[0].exchange)
        self.port=port

        _logger.debug('EmailSettings Initialized.')
        _logger.debug(f'''Sender: {self.sender}
        Recipient(s): {self.recipients}
        Reply-To: {self.reply_to}
        Server: {self.server}
        Port: {self.port}
        '''
        )

    def send_mail(self, subject=None, message_body=None, files=None):
        """Send an email

        Keyword Arguments:
            subject {str} -- Subject message. (default: {None})
            message_body {str} -- Email message body (default: {None})
            files {list of pathlib.Path} -- list of files to attach to email (default: {None})

        Raises:
            SMTPResponseException -- Raises SMTP errors
        """

        assert isinstance(self.recipients, list)

        msg=MIMEMultipart()
        msg['From']=self.sender
        msg['To']=COMMASPACE.join(self.recipients)
        msg['Date']=formatdate(localtime=True)
        msg['Subject']=subject
        msg.add_header('reply-to', self.reply_to)

        msg.attach(MIMEText(message_body))

        if files is not None:
            with open(files, "rb") as fil:
                part=MIMEApplication(
                    fil.read(),
                    Name=os.path.basename(files)
                )
            # After the file is closed
            part['Content-Disposition']=f'attachment; filename={os.path.basename(files)}'
            msg.attach(part)
        try:
            smtp=smtplib.SMTP(self.server, self.port)
            smtp.sendmail(self.sender, self.recipients, msg.as_string())
            smtp.close()
            _logger.debug('Email sent.')
        except SMTPResponseException as e:
            _logger.critical(f'SMTP Sendmail failed: {e.smtp_code} :: {e.smtp_error}')

def main():
    import inspect
    import time

    # Sleep 5 seconds to allow VSCode with code-runner and Anaconda to choose
    # the virtual environment and prevent that output from being captured as the sender or recipient inputs
    time.sleep(5)

    print('Instantiating LMCO_Email object.')

    emailer=lmco_email(
        sender=input("Sender email address: ")
        ,recipients=input("Recipient email address(es): ")
        ,reply_to=input("Reply-To email address(es): ")
        ,server='relay-lmi.ems.lmco.com'
        ,port=25
        )

    print(emailer.server)

    print('Object Instantiated.')
    print('Sending test email.')

    emailer.send_mail(
        subject='Testing LMCO_Email'
        ,message_body=f'''This was a test email from the LMCO_Email class.
        Sender: {emailer.sender}
        Recipient(s): {emailer.recipients}
        Reply-To: {emailer.reply_to}
        Server: {emailer.server}
        Port: {emailer.port}'''
        ,files=inspect.getfile(lmco_email)
    )

    print('Email sent.')
    print('End main().')

if __name__ == "__main__":
    main()