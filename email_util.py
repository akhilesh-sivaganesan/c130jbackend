import inspect
import time
import json
import requests
# Import Utility Functions
import sys
# sys.path.append('utils')
from lmco_email import lmco_email as le
# This for local email run
# import lmco_email as le

print("Hello World")

sender = 'vincent.v.do@lmco.com'
reply_back = 'vincent.v.do@lmco.com'


def send_feedback(feedback, request):

    # Try and get email details
    email_dict = {}
    try:
        email_dict['name'] = request.META['HTTP_X_DEADBOLT_NAME']
        email_dict['username'] = request.META['HTTP_X_DEADBOLT_PREFERRED_USERNAME']
        email_dict['email'] = request.META['HTTP_X_DEADBOLT_EMAIL']

    except Exception as e:
        email_dict['name'] = 'Vincent'
        email_dict['username'] = 'e447955'
        email_dict['email'] = 'vincent.v.do@lmco.com'

    recipients = f"vincent.v.do@lmco.com,{email_dict['email']}"
    reply_to = f"vincent.v.do@lmco.com,{email_dict['email']}"

    emailer = le.lmco_email(
        sender=sender, recipients=recipients, reply_to=reply_to, server='relay-lmi.ems.lmco.com', port=25
    )
    print(emailer.server)
    print('Sending test email')
    emailer.send_mail(
        subject=f'SHORTAGE APP UPDATE FROM {email_dict["name"]}', message_body=f'''
        
        SHORTAGE APP UPDATE FROM {email_dict["name"]}:

        NTID : {email_dict["username"]}

        
        FEEDBACK


        {feedback}


        Sender: {emailer.sender}
        Recipients(s): {emailer.recipients}
        Reply-To: {emailer.reply_to}
        Server: {emailer.server}
        Port: {emailer.port}
        '''
    )
    print("Email Sent")


def send_update_email(data):
    # Extract the NTIDs from the data
    ntids = data['ntid'].split(',')
    print("Searching for NTIDs to Email - SSL Bypass")
    # Make an API call to the EWP PersonService for each NTID to get the email addresses
    recipients = []
    for ntid in ntids:
        ewp_url = f"https://api-ewp.global.lmco.com/PersonService?Search={ntid}&APIKey=f3505421-a0de-4eec-ac44-fe7a24812d46&Output=JSON"
        response = requests.get(ewp_url, verify=False)
        ewp_data = json.loads(response.text)
        email = ewp_data[0]['Email']
        recipients.append(email)

    # Set up the email parameters
        sender = 'jawad.iqbal@lmco.com'
        reply_to = 'jawad.iqbal@lmco.com'
        subject = f"Shortage Update - Part Number: {data['part_number']}"
        message_body = f"""
        A shortage has been updated with new information. You can access the shortage info directly through this link:

        http://c-130j-shortages.apps.pgw2.us.lmco.com/editor?owner={data['owner']}&id={data['id']}

        Business Unit: {data['business_unit']}
        Ship: {data['ship']}
        TVE: {data['tve']}
        Part Number: {data['part_number']}
        Description: {data['description']}
        Assembly: {data['assembly']}
        Quantity: {data['qty']}
        Code: {data['code']}
        Owner: {data['owner']}
        Need Date: {data['need_date']}
        ECD: {data['ecd']}
        Previous ECD: {data['previous_ecd']}
        Impact: {data['impact']}
        Comment: {data['comment']}
        Status: {data['status']}
        Last Edit: {data['last_edit']}
        Added Date: {data['added_date']}
        On Board: {data['on_board']}
        Closed Date: {data['closed_date']}
        Manager: {data['manager']}

        Please review this information and take any necessary actions.
    """

    # Send a separate email to each recipient
    for recipient in recipients:
        emailer = le.lmco_email(
            sender=sender,
            recipients=recipient,
            reply_to=reply_to,
            server='relay-lmi.ems.lmco.com',
            port=25
        )
        emailer.send_mail(subject, message_body)

    print("Emails Sent")

# if __name__ == '__main__':
#     sender = 'vincent.v.do@lmco.com'
#     receiver = 'vincent.v.do@lmco.com'
#     send_email(sender,receiver)
