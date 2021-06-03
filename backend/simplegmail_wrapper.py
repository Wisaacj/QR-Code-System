from simplegmail import Gmail
import base64
class GreetingEmail:

    email_template: str = "Congratulations, {name} {surname}! You are going to Big Bertha!{br}{br}Below, you'll find attached a copy of your QR Code Ticket.{br}{br}Show it in the entrance and it's all gucci!!{br}{br}If you have any questions don't hesitate to contact us.{br}{br}Have fun,{br}{br}The Big Bertha Team"
    def __init__(self, name: str, surname:str, emailaddr: str, qr_code: str):
        self.name: str = name
        self.surname: str = surname
        self.emailaddr:str = emailaddr
        self.generate_tmp_png(qr_code)
        self.generate_email()
    
    def generate_tmp_png(self, encodedstring): #Generate temporary png image from the base64 string
        image = base64.urlsafe_b64decode(encodedstring)
        with open('QR_TICKET.png', 'wb') as f:
            f.write(image)
            
    def generate_email(self):
        self.email= self.email_template.format(name=self.name, surname=self.surname, br="<br>")
    
    def send(self):
        gmail_connector = Gmail()
        params: dict = {
        "to": self.emailaddr, 
        "sender": "antolbestg4@gmail.com",
        "subject": "Your Big Bertha Ticket",
        "msg_html": self.email,
        "attachments": ["QR_TICKET.png"],
        "signature": True
        }
        try:
            gmail_connector.send_message(**params)
            return True
        except Exception as e:
            print(str(e))
            return False
            
            
if __name__ == "__main__": #run tests
    test_qrcode:str = "iVBORw0KGgoAAAANSUhEUgAAAQkAAAEJAQAAAACvE+/JAAACnElEQVR4nO2ZS26mMBCEG7FgyRG4ibkYEkhcDG7iI7BkgdJTVT2RIJOZ2bYUvLAM/n4pjftR7Zj/byz2Ii/yIj8RuQxjGqzBY+eHaRr4ckiJYHVMdo7utfvo8QusvIuNjIg1BywaYcdp/QIYq26DlWmRGSZggjGrW+lhUXIEFrWcsLH/xaIkCP0F7/q10lU4XcM3LpUEiWjs9uM+fRewKRCNy/zDWixwCp/GaCREFI3ykrNhmis6iuNuUR7ksrPxtZ4WFk3muy9xCikRZDhWEusRl8UQl8UmQ2FZPSXCR3DMG2chh28P9+k9JYI0vCs147OrkpjKSXlEYx7kskhzhbsNOSbpZ2pOhHAcM8NvroDh7dZ7RVy2nhFB1YBv1N8rejY9hwYOGRFWuqOtkpdQbouC03QKKRGnvKT2oQAyOTpWdrcoEcLkERqzDSkEY2a6981fkiFYqZLQoqqs3O3h+OkQtBkbNhB+mOAvIYpOHkVGRNkCG3x3NhGca+1YrDMiHFSW2HAoCgQnbWP+84yI/GWtrsazMDXL26kyciJIyAi/QJjmVEnGh0V5EGeJxl+/GdUwfBsqg3X6ZlEm5FLeqKdyMVOGqZI8NWYehBLCpYYnNhwKyVBuQ0oErsLPLg3MkMRq+ezu8iEQ77JoDLWp/gM1pXm0/5kQJLc2kocEUMeeDudxtygT4lt4Nu9LmDJ2KuRyj8ZUiPojcHB0dkVyH/ui4NMgGjJGWfka1NvrZiIjonupmTpCJVDXaLyKiN/mQ4aQEOzkJDDU5eNxTYrEvdTGTk5dx8hobB4XPdmQyBanrib3EMdf/x+QCYkLCH52tfUVhe+PA0iCyF+Unzu+ZRHRbUpOJKIx+qPSS8OtLoGREfn3eJEXeZGfh/wCqy2NwMLyUm4AAAAASUVORK5CYII="
    
    test = GreetingEmail("Bob", "White", "anthony.dalamagas@gmail.com", test_qrcode)
    
    a = test.send()
    if (a):
        print("Sent successfuly.")
    else:
        print("Smth went wrong.")
    
    #print(test.generate_email())