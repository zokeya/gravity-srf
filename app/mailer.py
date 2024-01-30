import smtplib
import logging
from fastapi import Depends
from sqlalchemy.orm import Session

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate

import schedule
import time

from . import schemas, models,database, utils

def get_smtp_credentials(db: Session = Depends(database.get_db)):
    config = utils.get_email_config(db)
    return {
        "smtp_server": config.smtp_server,
        "smtp_port": config.smtp_port,
        "smtp_username": config.smtp_username,
        "smtp_password": config.smtp_password,
        "sender_email": config.sender_email,
    }

def send_email(subject, body, to_email, smtp_credentials, attachment_path=None, db: Session = Depends(database.get_db)):
    try:
        # Set up the email message
        msg = MIMEMultipart()
        msg['From'] = smtp_credentials['sender_email']  # Access sender_email directly
        msg['To'] = to_email
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        # Attach a file if provided (streaming)
        if attachment_path:
            with open(attachment_path, 'rb') as attachment:
                part = MIMEApplication(attachment.read(), Name='attachment')
                part['Content-Disposition'] = f'attachment; filename={attachment_path}'

                # Add the attachment part to the message without reading the entire file into memory
                msg.attach(part)

        # Connect to the SMTP server and send the email
        try:
            with smtplib.SMTP(smtp_credentials['smtp_server'], smtp_credentials['smtp_port']) as server:
                server.starttls()
                server.login(smtp_credentials['smtp_username'], smtp_credentials['smtp_password'])
                server.sendmail(msg['From'], to_email, msg.as_string())

                return None
        except Exception as e:
            return str(e)
    except Exception as e:
        logging.error(f"Error sending email: {e}")


def send_unsent_emails():
    with database.SessionLocal() as db:
        try:
            unsent_emails = utils.get_unsent_emails(db, 10)

            # Fetch SMTP credentials once
            smtp_credentials = get_smtp_credentials(db)

            for email in unsent_emails:
                error_details = send_email(email.subject, email.body, email.to_email, smtp_credentials, db=db)

                if error_details is None:
                    email.is_sent = True
                    email.error_details = None
                else:
                    email.error_details = error_details
                    email.is_sent = False

            db.commit()
        except Exception as e:
            logging.error(f"Error in sending pending mails: {e}")


# schedule.every(10).seconds.do(send_unsent_emails)

# while True:
#     schedule.run_pending()
#     time.sleep(1)