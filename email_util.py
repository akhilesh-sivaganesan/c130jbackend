import inspect
import time
# Import Utility Functions
import sys
# sys.path.append('utils')
from .lmco_email import lmco_email as le
# This for local email run
# import lmco_email as le

print("Hello World")

sender = 'jawad.iqbal@lmco.com'
reply_back = 'jawad.iqbal@lmco.com, eric.d.czarnecki@lmco.com'

def send_feedback(feedback,request):

    # Try and get email details
    email_dict = {}
    try:
        email_dict['name'] = request.META['HTTP_X_DEADBOLT_NAME']
        email_dict['username'] = request.META['HTTP_X_DEADBOLT_PREFERRED_USERNAME']
        email_dict['email'] = request.META['HTTP_X_DEADBOLT_EMAIL']

    except Exception as e :
        email_dict['name'] = 'Jawad'
        email_dict['username'] = 'e408811'
        email_dict['email'] = 'jawad.iqbal@lmco.com'

    recipients = f"jawad.iqbal@lmco.com,eric.d.czarnecki@lmco.com,{email_dict['email']}"
    reply_to = f"jawad.iqbal@lmco.com,eric.d.czarnecki@lmco.com,{email_dict['email']}"

    emailer = le.lmco_email(
        sender = sender
        ,recipients= recipients
        ,reply_to= reply_to
        ,server='relay-lmi.ems.lmco.com'
        ,port=25
    )
    print(emailer.server)
    print('Sending test email')
    emailer.send_mail(
        subject=f'6S APP FEEDBACK FROM {email_dict["name"]}'
        ,message_body=f'''
        
        6S APP FEEDBACK FROM {email_dict["name"]}:

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



def send_email(six_s_form,request,status=None):

    # Try and get email details fill with default information if there is any error
    email_dict = {}
    try:
        email_dict['status'] = status
        email_dict['name'] = request.META['HTTP_X_DEADBOLT_NAME']
        email_dict['username'] = request.META['HTTP_X_DEADBOLT_PREFERRED_USERNAME']
        email_dict['email'] = request.META['HTTP_X_DEADBOLT_EMAIL']

    except Exception as e :
        email_dict['status'] = status
        email_dict['name'] = 'Jawad'
        email_dict['username'] = 'e408811'
        email_dict['email'] = 'jawad.iqbal@lmco.com'



    # Instantiate email object
    emailer = le.lmco_email(
        sender = sender
        ,recipients= email_dict['email']
        ,reply_to= reply_back
        ,server='relay-lmi.ems.lmco.com'
        ,port=25
    )
    print(emailer.server)
    print('Sending test email')


    emailer.send_mail(
        subject='6S FORM CONFIRMATION'
        ,message_body=f'''
        
        Hello {email_dict['name']}, This is an email to confirm 6S App Form Submission/Update:

        
        6S SCORE {six_s_form.six_s_score}
        Date: {six_s_form.date_created}

        Line of Business: {six_s_form.line_of_business}
        Site: {six_s_form.site}
        Area: {six_s_form.area}
        Zone: {six_s_form.zone}
        PMT: {six_s_form.pmt}


        Sender: {emailer.sender}
        Recipients(s): {emailer.recipients}
        Reply-To: {emailer.reply_to}
        Server: {emailer.server}
        Port: {emailer.port}
        '''
    )
    print("Email Sent")




if __name__ == '__main__':
    sender = '6s_aero@lmco.com'
    receiver = 'jawad.iqbal@lmco.com'
    send_email(sender,receiver)