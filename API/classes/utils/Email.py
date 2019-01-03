import smtplib
from os.path import join
from API.models import MailServer, EmailTemplate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from API.settings.Globals import EMAIL_TEMPLATE_DIR, EMAIL_FROM_DOMAIN, EMAIL_TIMEOUT


class EmailHandler:
    website = ""
    api = ""
    mail_server = ""
    WELCOME_URL = ""
    CONFIRM_ACCOUNT_URL = ""
    LOGO_URL = ""
    FORGOT_PASSWORD_URL = ""

    def __init__(self, api, website="localhost"):
        self.mail_server = self.get_mail_server()
        self.website = website
        self.api = api
        self.WELCOME_URL = self.website
        self.FORGOT_PASSWORD_URL = self.api + "/api/v1/reset-password/"
        self.LOGO_URL = self.website + "/static/assets/images/INCA-Logo.png"
        self.CONFIRM_ACCOUNT_URL = self.api + "/api/v1/confirm-account/"

    def get_template(self, template):
        return EmailTemplate.objects.get(pk=template)

    def get_mail_server(self):
        return MailServer.objects.get(disabled=False)

    def replace_slugs_in_template(self, f, user):
        content = ""

        for line in f:
            line = line.replace("FIRSTNAME", user.user_profile.first_name.name)
            line = line.replace("FORGOT_PASSWORD_URL", self.FORGOT_PASSWORD_URL + str(user.uuid) + "/")
            line = line.replace("WELCOME_URL", self.WELCOME_URL)
            line = line.replace("LOGO_URL", self.LOGO_URL)
            line = line.replace("CONFIRM_ACCOUNT_URL", self.CONFIRM_ACCOUNT_URL + str(user.uuid) + "/")
            content += line

        return content

    def send_template(self, template_type, user):

        try:
            email_template = self.get_template(template_type)
        except Exception as error:
            print(error)
            return False

        msg = MIMEMultipart("alternative")
        msg['Subject'] = email_template.subject
        msg['To'] = "<" + user.user_profile.first_name.name + " " + user.user_profile.last_name.name + ">" + user.email
        msg['From'] = "<INCA Medical Support>" + email_template.from_address + "@" + EMAIL_FROM_DOMAIN

        try:
            f = open(join(EMAIL_TEMPLATE_DIR, str(email_template.text)), "r")
            content = self.replace_slugs_in_template(f, user)
            msg.attach(MIMEText(content, "plain"))
        except Exception as error:
            print(error)
            return False

        try:
            f = open(join(EMAIL_TEMPLATE_DIR, str(email_template.html)), "r")
            content = self.replace_slugs_in_template(f, user)
            msg.attach(MIMEText(content, "html"))
        except Exception as error:
            print(error)
            return False

        with smtplib.SMTP(host=self.mail_server.server,
                          port=self.mail_server.port,
                          timeout=EMAIL_TIMEOUT) as server:
            try:
                server.login(user=self.mail_server.username,
                             password=self.mail_server.password)
            except Exception as error:
                print("login")
                print(error)
                return False
            try:
                server.sendmail(from_addr=email_template.from_address,
                                to_addrs=user.email,
                                msg=msg.as_string()
                                )

            except Exception as error:
                print("send")
                print(error)
                return False
            server.quit()
        return True
