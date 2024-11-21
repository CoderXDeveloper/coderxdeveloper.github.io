from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

FIXED_RATE = 175
VALID_CURRENCIES = {
    "pokecoin": ["pokecoin", "pc"],
    "owo": ["owo", "o"]
}


def standardize_currency(currency):
    currency_lower = currency.lower()
    for standard, aliases in VALID_CURRENCIES.items():
        if currency_lower in aliases:
            return standard
    return None


def convert_currency(amount, from_currency, to_currency):
    if from_currency == "pokecoin" and to_currency == "owo":
        return amount * FIXED_RATE
    elif from_currency == "owo" and to_currency == "pokecoin":
        return amount / FIXED_RATE
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    amount = data.get("amount")
    from_currency = standardize_currency(data.get("from_currency"))
    to_currency = standardize_currency(data.get("to_currency"))

    if not from_currency or not to_currency:
        return jsonify({"error": "Invalid currency provided."}), 400

    try:
        converted_amount = convert_currency(amount, from_currency, to_currency)
        if converted_amount is None:
            return jsonify({"error": "Invalid conversion parameters."}), 400

        return jsonify({
            "converted_amount": round(converted_amount, 2),
            "from_currency": from_currency,
            "to_currency": to_currency
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
