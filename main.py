from flask import Flask, render_template, request, redirect, url_for
from backend.ticket_manager import TicketClass

app = Flask(__name__)

# Route for the ticket purchasing page
@app.route('/', methods=['GET', 'POST'])
def welcome_page():
    error = None

    # Getting the number of tickets remaining to be sold
    tickets_remaining = TicketClass.MAX_LIMIT_TICKETS - TicketClass.getNumSoldTickets()

    # Returning an error message if all the tickets have been sold
    if (tickets_remaining == 0):
        return render_template('/tickets/buy-tickets.html', error="No tickets remaining, better luck next time", tickets_remaining=tickets_remaining)

    if (request.method == "POST"):
        """
        - Use a paypal API to fufil the payment payment
        - Check if the payment was successfull
        - If so, continue and make the ticket
        """
        # Creating a new QR code for the user's ticket
        qr_code = TicketClass.createQRCode("127.0.0.1:5000/verify?id=", (request.form['floatingForename'], request.form['floatingSurname']))
        if (qr_code != ""):
            # Purchase was successful
            fullname = request.form['floatingForename'] + " " + request.form['floatingSurname']
            return render_template('/tickets/success.html', name=fullname, qr_code=qr_code)
        else:
            error = "Unsuccessful operation, please try again"

    return render_template('/tickets/buy-tickets.html', error=error, tickets_remaining=tickets_remaining)


@app.route('/verify')
def verification_page():
    # Verifying the identity of the ticket
    allow, name = TicketClass.verify_ticket(request.args.get('id'))

    if (allow):
        fullname = name[0] + " " + name[1]
        return render_template('/verify/verification.html', name=fullname)

    return render_template('/verify/verification.html', name="Fail")