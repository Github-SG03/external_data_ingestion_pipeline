import imaplib
import email
from src.ingestion.writer import write_to_s3

def run_smtp_etl(source, run_date, bucket):
    mail = imaplib.IMAP4_SSL(source["host"])
    mail.login(source["user"], source["password"])
    mail.select("inbox")

    _, data = mail.search(None, "ALL")
    for num in data[0].split():
        _, msg_data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        for part in msg.walk():
            if part.get_filename():
                content = part.get_payload(decode=True)
                key = f'{source["s3_prefix"]}/dt={run_date}/{part.get_filename()}'
                write_to_s3(bucket, key, content)
