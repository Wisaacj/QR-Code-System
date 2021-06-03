from flask import Flask, render_template, request, redirect, url_for, session
from backend.ticket_manager import TicketClass

import stripe

app = Flask(__name__)

# Adding STRIPE tokens to the app configuration
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_1CPqKqHEMYPL3pep8bzUadZQ'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_2dqyTdYE3bmQbslK8JQg3X9D'

# Setting up the STRIPE API key
stripe.api_key = app.config['STRIPE_SECRET_KEY']

# Route for the ticket purchasing page
@app.route('/', methods=['GET', 'POST'])
def index():
    # Getting the number of tickets remaining to be sold
    tickets_remaining = TicketClass.MAX_LIMIT_TICKETS - TicketClass.getNumSoldTickets()

    # Returning an error message if all the tickets have been sold
    if (tickets_remaining == 0):
        return render_template('/tickets/buy-tickets.html', error="NoTickets", tickets_remaining=tickets_remaining)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1Ixv2UDTPk3QaJIM1e6YzLrw',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True) + '?error=Fail',
    )

    return render_template('/tickets/buy-tickets.html',
        checkout_session_id=session['id'],
        checkout_public_key=app.config['STRIPE_PUBLIC_KEY'],
        tickets_remaining=tickets_remaining
    )

@app.route('/success', methods=['GET'])
def success():
    # Purchase was successful
    session_info = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    customer = stripe.Customer.retrieve(session_info.customer)

    # Parsing the customer's name
    fullname = customer.name
    if (len(fullname.split(" ")) > 1):
        forename, surname = fullname.split(" ")[0], fullname.split(" ")[1]
    else:
        forename, surname = fullname, ""

    # Checking to see if the user has refreshed the page
    if (request.args.get('session_id') == TicketClass.LAST_SESSION_ID):
        return render_template('/tickets/success.html', name="", qr_code="", refresh=True)

    # Creating a new QR code for the user's ticket
    qr_code = TicketClass.createQRCode("127.0.0.1:5000/verify?id=", (forename, surname))
    # Setting the last session id to the current id
    TicketClass.LAST_SESSION_ID = request.args.get('session_id')
    
    return render_template('/tickets/success.html', name=fullname, qr_code=qr_code)

@app.route('/verify')
def verification_page():
    # Verifying the identity of the ticket
    allow, name = TicketClass.verify_ticket(request.args.get('id'))

    if (allow):
        fullname = name[0] + " " + name[1]
        return render_template('/verify/verification.html', name=fullname)

    return render_template('/verify/verification.html', name="Fail")