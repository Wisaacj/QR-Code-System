from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Route for the ticket purchasing page
@app.route('/', methods=['GET', 'POST'])
def welcome_page():
    error = None

    if (request.method == "POST"):
        # Creating a new ticket for the user
        newTicket = TicketClass(request.form['floatingForename'], request.form['floatingSurname'])
        # Generating QR code for the ticket
        qr_code = newTicket.createQRCode()
        if (qr_code != ""):
            # Purchase was successful
            return render_template('/tickets/success.html', name=request.form['floatingForename'] + request.form['floatingSurname'])
        else:
            error = "Unsuccessful operation, please try again"
            
    return render_template('/tickets/buy-tickets.html', error=error)


@app.route('/verify?id=<id>')
def verification_page(id):
    # Class for checking the identity of the QR code
    # allow, name = verify_id(id)
    allow = false
    name = ""
    if (allow):
        return render_template('/verify/verification.html', name=name)
    else:
        return render_template('/verify/verification.html', name="Fail")