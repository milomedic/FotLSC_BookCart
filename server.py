import os
import stripe
from flask import Flask, request, redirect

app = Flask(__name__)

stripe.api_key = os.getenv("FotLSC_STRIPE_SECRET_KEY")



PRICE_IDS = {
    "hardback": "price_1SlZaDAn6MMwMYK28ZSrqwcW",
    "paperback": "price_1SlZXzAn6MMwMYK2aW6XLCml",
    "children": "price_1SlZbiAn6MMwMYK2yEpuWXBV",
    "dvd": "price_1SpGHkAn6MMwMYK2ejkZSICJ"
}

@app.route("/checkout", methods=["POST"])
def checkout():
    line_items = []

    for key, price_id in PRICE_IDS.items():
        qty = int(request.form.get(key, 0))
        if qty > 0:
            line_items.append({
                "price": price_id,
                "quantity": qty
            })

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=line_items,
        success_url="https://yourdomain.com/success",
        cancel_url="https://yourdomain.com/cancel",
        submit_type="pay",
        custom_fields=[
            {
                "key": "tip",
                "label": {"type": "custom", "custom": "Tip / Donation"},
                "type": "numeric",
                "numeric": {"minimum": 0}
            }
        ],
        metadata={"tip_field": "enabled"}
    )

    return redirect(session.url, code=303)
