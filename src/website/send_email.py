import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_notification(estateNum: int):
    # Set up the sender and receiver email addresses
    sender_email = "plusaqar@gmail.com"
    receiver_email = "aqarplus2024@gmail.com"
    password = "mvmo flrv tqnv wzkm"  # Use App Password if 2FA is enabled

    # estateNum = 15 # change it
    subject = f"لقد حصلت على عقار جديد رقم {estateNum}"
    body = "تفحص التطبيق!"

    # Create the MIMEMultipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    estateNum = 15  # change it
    message["Subject"] = subject

    # Add email body
    message.attach(MIMEText(body, "plain"))

    # Set up the SMTP server
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Start TLS for security
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:  # # Create the MIMEMultipart message
        print(f"Error: {e}")
    finally:
        server.quit()
