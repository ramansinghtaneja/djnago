import pandas as pd
import smtplib
from smtplib import SMTPException
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import environ


env = environ.Env()


environ.Env.read_env()

MAILSERVER = env('MAILSERVER')
MAILPORT = env('MAILPORT')
DEBUG = env.bool('DEBUG', default=False)


SUBJECT= "Interview Scheduled with Zinnia"
ATTACHMENTS=[]
SENDER = 'hr@zinnia.com'
CC=['anant.vijay@zinnia.com']
RECEIVERS=['abhay.prajapati@zinnia.com','anant.vijay@zinnia.com','ramanjot.singh@zinnia.com']

def sendemail(mail_content,subject,df,RECEIVERS,ATTACHMENTS=[]):   
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = SENDER
    message['To'] = ", ".join(RECEIVERS)
    message['Cc']= ", ".join(CC)
    message.attach(MIMEText(mail_content, 'html'))
    
    for filename in ATTACHMENTS:
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read()) 
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {filename}",)
        message.attach(part)

    try:
        server = smtplib.SMTP(MAILSERVER,MAILPORT)      
        server.sendmail(SENDER, RECEIVERS, message.as_string())
        server.quit()
        status=True
        return status
    except Exception as e:
        status=False
        return str(e)


# mail_content="""
# <html>
#   <head></head>
#   <body>
#   Dear Candidate, <br>
#   Congratulation! Your interview has been scheduled with Zinnia. Please refer to the following details raman. <br><br>
#   {0}<br><br>
#    Regards,<br>
#    HR Zinnia
#   </body>
# </html>
# """.format(styled_dfc.to_html())


# if len(df)>0:
#     print('email sending process begins')
#     res=sendemail(mail_content, SUBJECT, df, RECEIVERS)
#     print(res)
#     print('email sending process ends')


# def send_email(styled_dfc):

#     mail_content="""
#     <html>
#     <head></head>
#     <body>
#     Dear Candidate, <br>
#     Congratulation! Your interview has been scheduled with Zinnia. Please refer to the following details raman. <br><br>
#     {0}<br><br>
#     Regards,<br>
#     HR Zinnia
#     </body>
#     </html>
#     """.format(styled_dfc.to_html())

#     if len(styled_dfc)>0:
#         print('email sending process begins')
#         res=sendemail(mail_content, SUBJECT, df, RECEIVERS)
#         print(res)
#         print('email sending process ends')




