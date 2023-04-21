from tools.prepare_data import example_data_drift
from tools.send_email_attachment import EmailAttachment, send_email_attachment
from tools.send_email_basic import send_email_basic
from tools.send_email_formatted import send_email_formatted

RECIPIENT_LIST = ["your.email@here.com"]
PROJECT_NAME = "Example Adult Education"
LINK_URL = "www.your-url.com"


is_alert, html, html_bytes = example_data_drift()


def formatted_email_example():
    if is_alert:
        send_email_formatted(
            project_name=PROJECT_NAME, link_url=LINK_URL, recipient_list=RECIPIENT_LIST
        )


def email_attachment_example():
    if is_alert:
        send_email_attachment(
            project_name=PROJECT_NAME,
            link_url=LINK_URL,
            recipient_list=RECIPIENT_LIST,
            attachment_list=[
                EmailAttachment(
                    file_name="data_drift.html",
                    content=html_bytes,
                ),
            ],
        )


def basic_email():
    if is_alert:
        send_email_basic(
            project_name=PROJECT_NAME,
            link_url=LINK_URL,
            recipient_list=RECIPIENT_LIST,
        )


if __name__ == "__main__":
    basic_email()
