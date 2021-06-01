from typing import Union
import pyqrcode
import png
import uuid
import sqlite3

class TicketClass:
    MAX_LIMIT_TICKETS: int = 50 #store max number of tickets.

    @staticmethod
    def createRandomHash() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def setMaxTickets(num: int) -> None: #set the max amount of tickets.
        if num > 0:
            MAX_LIMIT_TICKETS = num

    @staticmethod
    def setCheckedIn(tid: str, checkedIn: int =1) -> bool: #Set Check-In status given a valid ticked id; returns true if update was succesful. False on any error.
        conn = sqlite3.connect("C:\\Users\\Will\Documents\\GitHub\\QR-Code-System\\backend\\issued_tickets.db")
        try:
            with conn:
                conn.execute("UPDATE Tickets SET CheckedIn=? WHERE TicketID=?",(checkedIn, tid))
        except Exception as ex:
            print(str(ex))
            return False
        finally:
            conn.close()

        return True

    @staticmethod
    def createQRCode(url: str, db_values: tuple) -> str: #adds a new ticket to the db and returns a qr code for it.
        randomID: str = TicketClass.createRandomHash()
        url += randomID
        qr_encoded_url = pyqrcode.create(url)
        con = sqlite3.connect("C:\\Users\\Will\Documents\\GitHub\\QR-Code-System\\backend\\issued_tickets.db")
        try:
            if(TicketClass.getNumSoldTickets() >= TicketClass.MAX_LIMIT_TICKETS):
                raise Exception("Sold Out!")
            with con:
                con.execute("INSERT INTO Tickets(FirstName, LastName,TicketID) VALUES(?,?,?)",(db_values[0], db_values[1],randomID))
        except Exception as ex:
            print(f"Smth went wrong! {str(ex)}")
            return ""
        finally:
            con.close()

        return f"data:image/png;base64,{qr_encoded_url.png_as_base64_str(scale=5, quiet_zone=6)}"

    @staticmethod
    def verify_ticket(tid: str) -> Union[bool,tuple]: #verifies if a ticket id is valid i.e. present in the DB.
        conn = sqlite3.connect("C:\\Users\\Will\Documents\\GitHub\\QR-Code-System\\backend\\issued_tickets.db")
        cursor = conn.cursor()
        cursor.execute("SELECT FirstName,LastName,CheckedIn FROM Tickets WHERE TicketID=?", (tid,))
        record: tuple = cursor.fetchone()

        entry_info = None

        if record is None: #If not found in DB
            entry_info = False, ("","")

        elif record[2] == 1: #If Already Checked In.
            entry_info = False, (record[0], record[1])
        else:
            entry_info = True,(record[0], record[1]) #If found in db AND NOT CheckedIn.

        if entry_info is None:
            entry_info = (False, ("",""))

        conn.close()
        return entry_info

    @staticmethod
    def getNumSoldTickets() -> int: #returns the number of tickets sold.
        conn = sqlite3.connect("C:\\Users\\Will\Documents\\GitHub\\QR-Code-System\\backend\\issued_tickets.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(TicketID) FROM Tickets")
        sold: int = cursor.fetchone()[0]

        if sold is None:
            return 0

        conn.close()
        return sold


#Run tests if script is accessed directly.
if __name__ == "__main__":

    test_entries = (
    ("Anthony", "Dalamagas"),
    ("John", "Doe"),
    ("John", "Doe"),
    ("Bob", "White")
    )

    for entry in test_entries:
        qr_code_base64 = TicketClass.createQRCode("https://example.com?id=", entry)
        if qr_code_base64 != "":
            print(entry)
            print(qr_code_base64)
            print()
        else:
            print(f"Failure adding {entry[0]} {entry[1]}")

    TestID1 = "<Test a valid ID here>"
    print(f"Verifying {TestID1}")
    print(TicketClass.verify_ticket(TestID1))

    print()

    print("Verifying ILikeSpaghettiSomuch0799ak95jdl8")
    print(TicketClass.verify_ticket("ILikeSpaghettiSomuch0799ak95jdl8"))

    print()

    print(TicketClass.setCheckedIn("<Test a CheckedIn ID Here>"))

    TestID2 ="<Test a CheckedIn ID Here>"
    print(f"Verifying {TestID2}")
    print(TicketClass.verify_ticket(TestID2))

    print()

    print(f"Tickets Sold: {TicketClass.getNumSoldTickets()}")
