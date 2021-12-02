import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def emaildaily():
    file = "daily_time_heart_rate.png"
    subject = "health data"
    body = "daily heart rate"
    sender_email = "eptprogramming2021@gmail.com"
    receiver_email = open("physician_email.txt", 'r').read() 
    password = "programmingEPT2021"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email
    message.attach(MIMEText(body, "plain"))
    with open(file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file}",
        )
    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


def emailweek():
    file "weekly_heart_rate.png"
    subject = "Health data"
    body = "weekly heart rate"
    sender_email = "eptprogramming2021@gmail.com"
    receiver_email = open("physician_email.txt", 'r').read() 
    password = "programmingEPT2021"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email
    message.attach(MIMEText(body, "plain"))
    with open(file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file}",
        )
    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


def emailtool(message):
    files = ["data.csv", "all_time_heart_rate.png", "ranges_heart_rate.png", 
             "three_line_plot_accelerometer.png", "three_dimension_plot_accelerometer.png", "force_plot.png"]
    subject = "Health data"
    body = message
    sender_email = "eptprogramming2021@gmail.com"
    receiver_email = open("physician_email.txt", 'r').read() 
    password = "programmingEPT2021"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email
    message.attach(MIMEText(body, "plain"))
    for file in files:
        with open(file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file}",
            )
        message.attach(part)
        text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
