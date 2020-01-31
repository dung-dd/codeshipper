# coding: utf-8

import smtplib
from email.message import EmailMessage
from email.headerregistry import Address

sender_email_password = "Y29kZXNoaXBwZXI"
sender_email = "codeshipper@gmail.com"
receiver_email = "btdungbk@gmail.com"
smtp_host = ("smtp.gmail.com", 587)

class SendEmail():

    def __init__(self, project_name, project_version, content):
        self.project_name = project_name
        self.project_version = project_version
        self.content = content
        self.send()

    def send(self):
        email_obj = EmailMessage()
        # email_obj.set_content("""
        #     <h1>Xin chao</h1>
        #     <center><button onclick=>Click Me</button></center>
        # """)
        email_content = f"""
            <h4>Project: {self.project_name}</h4>
            <h4>Version: {self.project_version}</h4>
            <p>Result: {self.content}</p>
        """
        email_obj.set_content(email_content)


        email_obj.set_type("text/html")
        email_obj["Subject"] = "Kết quả nâng cấp"
        email_obj["From"] = Address (display_name="CS Admin", addr_spec=sender_email)
        email_obj["To"] = Address(addr_spec="btdungbk@gmail.com")
        
        """ print email """
        for key in email_obj.keys():
            print (key +": ", email_obj.get(key))
        print ("Content: ", email_obj.get_content())
        
        try:
            smtp_server = smtplib.SMTP("smtp.gmail.com", 587) 
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_email_password)
            smtp_server.sendmail(sender_email, receiver_email, email_obj.as_string())
            smtp_server.quit()
        except Exception as e:
            print (e) 