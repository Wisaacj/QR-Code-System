import sqlite3
conn = sqlite3.connect('issued_tickets.db')
cursor = conn.cursor()

create_table_queries = (
'''
CREATE TABLE Tickets (
    FirstName TEXT NOT NULL,
    LastName TEXT,
    TicketID TEXT NOT NULL,
    CheckedIn INT DEFAULT 0,
    PRIMARY KEY (TicketID)
)
''',

'''
CREATE TABLE Other (
    OtherData TEXT
)
'''
)

for query in create_table_queries:
    conn.execute(query)
    conn.commit()

conn.close()
    

    
