import pyqrcode
import png
import uuid
import sqlite3

class TicketClass:
    
    def __init__(self, name: str, lastname: str): #name, lastname = user info to store in sqlite db_fields
        self.url = "https://example.com/verify?id=" #Ticket Verification URL
        self.name = name
        self.lastname = lastname
     
    def createRandomHash(self) -> str:
        return uuid.uuid4().hex
    
    def createQRCode(self) -> str: #adds a new ticket to the db and returns a qr code for it.
        randomID = self.createRandomHash()
        randomURL = self.url + randomID
        qr_encoded_url = pyqrcode.create(randomURL)
        con = sqlite3.connect("issued_tickets.db")
        try:
            with con:
                con.execute("INSERT INTO Tickets(FirstName, LastName,TicketID) VALUES(?,?,?)",(self.name,self.lastname,randomID))
        except Exception as ex:
            print(f"Smth went wrong! {str(ex)}")
            return ""
        finally:
            con.close()
        
        return f"data:image/png;base64,{qr_encoded_url.png_as_base64_str(scale=5, quiet_zone=6)}"
        

if __name__ == "__main__":
    test_entries = (
    ("Anthony", "Dalamagas"),
    ("John", "Doe"),
    ("John", "Doe"),
    ("Bob", "White")
    )
    
    for entry in test_entries:
        ticket = TicketClass(entry[0], entry[1])
        qr_code_base64 = ticket.createQRCode()
        if qr_code_base64 != "":
            print(qr_code_base64)
        else:
            print(f"Failure adding {entry[0]} {entry[1]}")
        