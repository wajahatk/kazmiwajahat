from os import getenv
from ssl import create_default_context
from smtplib import SMTP, SMTPException


# ---------------------------------------------------------------------------- #
def send_error_email(error_to_send):
        smtp_server = "smtp.gmail.com"
        port = 587 # For starttls
        sender = getenv('SENDER_EMAIL')
        receiver = getenv('REC_EMAIL')
        pw = getenv('SENDER_PW')
        msg = f"""\
        Subject: JoshBot9000 Error

        Error: {error_to_send}."""
        context = create_default_context()
        try:
            server = SMTP(smtp_server, port)
            server.starttls(context=context)
            server.login(sender, pw)
            server.sendmail(sender, receiver, msg)         
            print(f"…÷÷÷ Sent error email to {sender} ÷÷÷…")
        except SMTPException:
            print("Error: unable to send email")
        finally:
            server.quit()


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    send_error_email()