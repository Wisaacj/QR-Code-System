# QR Code System

## Database

Fields required for the database:

- Forename --- VARCHAR
- Surname --- VARCHAR
- Email --- EMAIL
- Hash --- VARCHAR
- CheckedIn --- BOOLEAN
- NoTicketsSold --- INTEGER

## Routes


- Splashpage, which is the purchase ticket page.
- Verifcation, which indicates whether the person should be allowed in or not (RICKY)
- Contact/Report problem page, for any issues

## Email Message

Included within the email message:

- QR Code
- A thank you message for buying
- Time of the event

## Additional functionality required

- Clear the database
- Limit the number of tickets
