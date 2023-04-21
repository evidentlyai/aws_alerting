from typing import List

import boto3
import jinja2
from botocore.exceptions import ClientError


def render_email_template(
    project_name: str,
    link_url: str = "",
    template_file: str = "main.html",
) -> str:  # pragma: no cover -> too long html file
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("src/email_template"),
        autoescape=jinja2.select_autoescape(
            enabled_extensions=["html"], default_for_string=True
        ),
    )
    template = env.get_template(template_file)

    return template.render(project_name=project_name, link_url=link_url)


def send_email_formatted(
    project_name: str,
    recipient_list: List[str],
    link_url: str = "",
) -> None:
    # Note: send email **must be** verified within SES service
    SENDER = "MLOps Monitoring Alert <verified-sender-email@here.com>"
    SUBJECT = f"[Monitoring Alert] {project_name}"
    # The HTML body of the email.
    BODY_HTML = render_email_template(project_name=project_name, link_url=link_url)

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
