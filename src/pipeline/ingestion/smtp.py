import csv
import email
import imaplib
from typing import Dict, List, Optional


def run_smtp_ingestion(source: Dict, run_date: str, bucket: str) -> List[Dict]:
    """
    Ingest CSV attachments from email via IMAP.
    CI-safe (lazy runtime behavior).
    """

    host = source["host"]
    username = source["username"]
    password = source["password"]
    mailbox = source.get("mailbox", "INBOX")

    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select(mailbox)

    _, data = mail.search(None, "ALL")
    mail_ids = data[0].split() if data and data[0] else []

    records: List[Dict] = []

    for mail_id in mail_ids[-5:]:  # limit recent emails
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        if status != "OK" or not msg_data:
            continue

        raw_msg: Optional[bytes] = (
            msg_data[0][1] if isinstance(msg_data[0], tuple) else None
        )
        if not raw_msg:
            continue

        msg = email.message_from_bytes(raw_msg)

        for part in msg.walk():
            if part.get_content_type() == "text/csv":
                payload = part.get_payload(decode=True)
                if not isinstance(payload, (bytes, bytearray)):
                    continue

                content = payload.decode("utf-8", errors="ignore")
                reader = csv.DictReader(content.splitlines())
                records.extend(list(reader))

    mail.logout()
    return records
