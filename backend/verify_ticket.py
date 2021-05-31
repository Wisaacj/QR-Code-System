import sqlite3
from typing import Union
conn = sqlite3.connect('issued_tickets.db')

def verify_ticket_id(tid: str) -> Union[bool,tuple]:
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT FirstName,LastName,CheckedIn FROM Tickets WHERE TicketID=?", (tid,))
        record = cursor.fetchone()
        if record is None: #If not found in DB
            return False, ("","")
        
        if record[2] == 1: #If Already Checked In.
            return False, (record[0], record[1])
        
        return True,(record[0], record[1]) #If found in db AND NOT CheckedIn.
            
    
if __name__ == "__main__": #Tests
    print("Verifying 421fa46290764a40950135ec75bd2e7e")
    print(verify_ticket_id("421fa46290764a40950135ec75bd2e7e"))
    
    print()
    
    print("Verifying ILikeSpaghettiSomuch0799ak95jdl8")
    print(verify_ticket_id("ILikeSpaghettiSomuch0799ak95jdl8"))
    
    print()
    
    print("Verifying 38095f73663549ce957699dfaa77799d")
    print(verify_ticket_id("38095f73663549ce957699dfaa77799d"))
    