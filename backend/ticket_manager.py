from typing import Union
import pyqrcode
import png
import uuid
import sqlite3
import os

class TicketClass:

    def __init__(self):
        file_path: str = os.path.realpath(__file__)
        dir_path: str = file_path[0:file_path.rindex('\\')]
        DB_path: str = f"{dir_path}\issued_tickets.db" 
        self.conn: Connection = sqlite3.connect(DB_path)
        self.cursor: Cursor = self.conn.cursor()
        self.MAX_LIMIT_TICKETS: int = 50 #store max number of tickets.

    def createRandomHash(self) -> str:
        return uuid.uuid4().hex


    def setMaxTickets(self, num: int) -> None: #set the max amount of tickets.
        if (num > 0):
            self.MAX_LIMIT_TICKETS = num
    
    def closeConnection(self) -> None: #closes the database connection.
        self.conn.close()
        self.conn = None

    def setCheckedIn(self, tid: str, checkedIn: int =1) -> bool: #Set Check-In status given a valid ticked id; returns true if update was succesful. False on any error.
        try:
            with self.conn:
                self.conn.execute("UPDATE Tickets SET CheckedIn=? WHERE TicketID=?",(checkedIn, tid))
        except Exception as ex:
            print(str(ex))
            return False
        
        return True


    def createQRCode(self, url: str, db_values: tuple) -> str: #adds a new ticket to the db and returns a qr code for it.
        randomID: str = self.createRandomHash()
        url += randomID
        qr_encoded_url = pyqrcode.create(url)
        try:
            if(self.getNumSoldTickets() >= self.MAX_LIMIT_TICKETS):
                raise Exception("MAX_LIMIT_TICKETS reached.")
            with self.conn:
                self.conn.execute("INSERT INTO Tickets(FirstName, LastName,TicketID) VALUES(?,?,?)",(db_values[0], db_values[1],randomID))
        except Exception as ex:
            print(str(ex))
            return ""

        return f"data:image/png;base64,{qr_encoded_url.png_as_base64_str(scale=5, quiet_zone=6)}"


    def verify_ticket(self, tid: str) -> Union[bool,tuple]: #verifies if a ticket id is valid i.e. present in the DB.
        self.cursor.execute("SELECT FirstName,LastName,CheckedIn FROM Tickets WHERE TicketID=?", (tid,))
        record: tuple = self.cursor.fetchone()

        entry_info = None

        if record is None: #If not found in DB
            entry_info = False, ("","")

        elif record[2] == 1: #If Already Checked In.
            entry_info = False, (record[0], record[1])
        else:
            entry_info = True,(record[0], record[1]) #If found in db AND NOT CheckedIn.

        if entry_info is None:
            entry_info = (False, ("",""))

        return entry_info


    def getNumSoldTickets(self) -> int: #returns the number of tickets sold.
        self.cursor.execute("SELECT COUNT(TicketID) FROM Tickets")
        sold: int = self.cursor.fetchone()[0]

        if sold is None:
            return 0

        return sold


#Run tests if script is accessed directly.
if __name__ == "__main__":

    test_entries = (
    ("Anthony", "Dalamagas"),
    ("John", "Doe"),
    ("John", "Doe"),
    ("Bob", "White")
    )
    
    ticketmgr = TicketClass()
    for entry in test_entries:
        qr_code_base64 = ticketmgr.createQRCode("https://example.com?id=", entry)
        if qr_code_base64 != "":
            print(entry)
            print(qr_code_base64)
            print()
        else:
            print(f"Failure adding {entry[0]} {entry[1]}")

    TestID1 = "<Test a valid ID here>"
    print(f"Verifying {TestID1}")
    print(ticketmgr.verify_ticket(TestID1))

    print()

    print("Verifying ILikeSpaghettiSomuch0799ak95jdl8")
    print(ticketmgr.verify_ticket("ILikeSpaghettiSomuch0799ak95jdl8"))

    print()

    print(ticketmgr.setCheckedIn("<Test a CheckedIn ID Here>"))

    TestID2 ="<Test a CheckedIn ID Here>"
    print(f"Verifying {TestID2}")
    print(ticketmgr.verify_ticket(TestID2))

    print()

    print(f"Tickets Sold: {ticketmgr.getNumSoldTickets()}")
    
    ticketmgr.closeConnection()
