#!/usr/bin/python3
import sendgrid

from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId)

def send(filename, job, city, email_receiver, sendgrid_api_key, sendgrid_email_sender):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)

        message = Mail(
            from_email = sendgrid_email_sender,
            to_emails = email_receiver.replace(',', ''),
            subject = f"LinkedIn: {job} jobs in {city} (Weekly).",
            html_content = f"Automated report for {job} jobs in {city} generated on {datetime.datetime.now()}."
        )

        with open(filename, 'rb') as f:
            data = f.read()
            f.close()
        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType('application/csv')
        attachment.file_name = FileName(filename)
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId('')
        message.attachment = attachment

        response = sg.client.mail.send.post(request_body=message.get())

        print(f"\n\033[1m📩 Email sent successfully to {email_receiver}\033[0m")

    except Exception as e:
        print("Error:", e)
        print("\n\033[1m❌ An error occurred while trying to send the email!\033[0m")
