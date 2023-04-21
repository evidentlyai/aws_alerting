from typing import List

import boto3
from botocore.exceptions import ClientError


def send_email_basic(
    project_name: str,
    recipient_list: List[str],
    link_url: str = "",
) -> None:
    # Note: send email **must be** verified within SES service
    SENDER = "MLOps Monitoring Alert <verified-sender-email@here.com>"
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
            <p>
                <a href='{link_url}'>Link to the Reports</a>
            </p>"""

    BODY_HTML += """\
    </body>
    </html>
    """

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client("ses", "eu-west-1")

    # Send email
    try:
        response = client.send_email(
            Destination={
                "ToAddresses": [
                    *recipient_list,
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": BODY_HTML,
                    },
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": SUBJECT,
                },
            },
            Source=SENDER,
        )

    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        print(f"Email sent to the following recipients: {recipient_list}"),
        print(f"Message ID: {response['MessageId']}")
