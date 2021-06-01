import sqlite3
conn = sqlite3.connect('issued_tickets.db')
cursor = conn.cursor()


query = '''
CREATE TABLE Tickets (
    FirstName TEXT NOT NULL,
    LastName TEXT,
    TicketID TEXT NOT NULL,
    CheckedIn INT DEFAULT 0,
    PRIMARY KEY (TicketID)
)
'''

conn.execute(query)
conn.commit()
conn.close()
    

    
