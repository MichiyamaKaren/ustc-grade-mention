import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def send_qq_mail(sender, password, sender_name, reciever, reciever_name, title, message):
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = formataddr([sender_name, sender])
    msg['To'] = formataddr([reciever_name, reciever])
    msg['Subject'] = title

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(sender, password)
    server.sendmail(sender, [reciever], msg.as_string())
    server.quit()
