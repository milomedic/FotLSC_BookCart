from flask import Flask, request, redirect, send_from_directory
import stripe
from config import FotLSC_STRIPE_SECRET_KEY

app = Flask(__name__)

key = FotLSC_STRIPE_SECRET_KEY
if not key:
    raise Exception("FotLSC_STRIPE_SECRET_KEY is missing")
stripe.api_key = key


PRICE_IDS = {
    "hardback": "price_1SlZaDAn6MMwMYK28ZSrqwcW",
    "paperbackLarge": "price_1SlZXzAn6MMwMYK2aW6XLCml",
    "paperbackSmall": "price_1T6tS9An6MMwMYK2yKJlwIsU",
    "children": "price_1SlZbiAn6MMwMYK2yEpuWXBV",
    "dvd_cd": "price_1SpGHkAn6MMwMYK2ejkZSICJ",
    "boardgame": "price_1T6tUeAn6MMwMYK2d7Jrf2eh",
    "totebag": "price_1T6tVxAn6MMwMYK2f8JSHlB2"

}

# Route 1: Homepage
@app.route("/")

def home():
    return send_from_directory(".", "index.html")


# Route 2: Checkout
@app.route("/checkout", methods=["POST"])

def checkout():
    try:
        line_items = []

        # Add selected items to line_items
        for key, price_id in PRICE_IDS.items():
            qty = int(request.form.get(key, 0))
            if qty > 0:
                line_items.append({
                    "price": price_id,
                    "quantity": qty
                })

        # Handle tip/donation
        tip = request.form.get("tip", "0")
        try:
            tip_value = float(tip)
            if tip_value > 0:
                line_items.append({
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "Tip / Donation"},
                        "unit_amount": int(tip_value * 100)  # convert dollars to cents
                    },
                    "quantity": 1
                })
        except ValueError:
            # If tip is not a number, ignore it
            pass

         # Ensure at least one item is selected
        if not line_items:
            return "<h1>No items selected</h1>"

        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            success_url="https://scrlibraryfriends.pythonanywhere.com/success",
            cancel_url="https://scrlibraryfriends.pythonanywhere.com",
            submit_type="pay"
        )
        return redirect(session.url, code=303)

    except Exception as e:
        return f"<h1>Stripe error</h1><pre>{str(e)}</pre>"

# Route 3: success
@app.route("/success")
def success():
    return """
    <html>
        <head>
            <title>Payment Successful</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: Arial; text-align: center; margin: 30px;">
            <div>
                <img src="https://images.squarespace-cdn.com/content/65ca235117c67c6a4c85578b/0ea921ac-48fb-4b61-894f-8c2becba97c4/bookmark+logo+-+green.png?format=1000w&content-type=image%2Fpng"
                     style="max-width: 150px;">
            </div>
            <h1>Thank you!</h1>
            <p>Your payment was successful.</p>
            <p>We appreciate your support of the library.</p>
            <br>
            <a href="/" style="font-size: 18px;">← Return to Book Cart</a>
        </body>
    </html>
    """
