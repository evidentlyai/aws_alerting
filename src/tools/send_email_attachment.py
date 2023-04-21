from dataclasses import dataclass
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

import boto3
from botocore.exceptions import ClientError


@dataclass
class EmailAttachment:
    file_name: str
    content: bytes


def __attach_attachment_to_msg(
    attachment: EmailAttachment, msg_object: MIMEMultipart
) -> None:
    att = MIMEApplication(attachment.content)

    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    att.add_header("Content-Disposition", "attachment", filename=attachment.file_name)

    # Add the attachment to the parent container.
    msg_object.attach(att)


def send_email_attachment(
    project_name: str,
    recipient_list: List[str],
    link_url: str = "",
    attachment_list: List[EmailAttachment] = [],
) -> None:
    # Note: send email **must be** verified within SES service
    SENDER = "MLOps Monitoring Alert <verified-sender-email@here.com>"

    # The subject line for the email.
    SUBJECT = f"[Monitoring Alert] {project_name}"

    # The HTML body of the email.
    BODY_HTML: str = """\
    <html>
    <head></head>
    <body>
    <h1>Data Drift / Performance degradation identified!</h1>
    <p>Please see the attached files for the <b>Data Monitoring Reports</b>.</p>
    """

    if link_url:
        BODY_HTML += f"""\
            <p><a href='{link_url}'>Link to the Report</a><br>
            </p>"""

    BODY_HTML += """\
    </body>
    </html>
    """

    # The character encoding for the email.
    CHARSET = "utf-8"

    # Create a new SES resource and specify a region.
    client = boto3.client("ses")

    # Create a multipart/mixed parent container.
    msg = MIMEMultipart("mixed")
    # Add subject, from and to lines.
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = ", ".join(recipient_list)

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart("alternative")

    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    html_part = MIMEText(BODY_HTML, "html", CHARSET)

    # Add the text and HTML parts to the child container.
    msg_body.attach(html_part)

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    # Define the attachment part and encode it using MIMEApplication
    # > Note: only works if calling a function
    if attachment_list:
        [__attach_attachment_to_msg(att, msg) for att in attachment_list]

    try:
        # Provide the contents of the email.
        print(f"Sending email to: {recipient_list}")
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[*recipient_list],
            RawMessage={
                "Data": msg.as_string(),
            },
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        print("Email sent! Message ID:")
        print(response["MessageId"])
