import smtplib
from email.mime.text import MIMEText


class SKEmail:
    ''' Constructor for this class. '''
    def __init__(self):
        self.smtpserver = "smtp.gmail.com"

    def sendMail(Subject,FromAddress,ToAddress,smftpLoginUser,smtpCredential):
        ''' Send Mail. '''
        msg = MIMEText(Subject)
        msg["Subject"] = Subject
        msg["From"] = FromAddress
        msg["To"] = To
        with smtplib.SMTP(smtpserver, 587) as server:
            server.ehlo()
            server.starttls()
            server.login(smftpLoginUser, smtpCredential)
            server.sendmail(FromAddress, ToAddress, msg.as_string())