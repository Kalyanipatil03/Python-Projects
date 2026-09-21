import time
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

POPULAR_CURRENCIES = {
    "USD": "United States Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "INR": "Indian Rupee",
    "CAD": "Canadian Dollar",
    "AUD": "Australian Dollar",
    "JPY": "Japanese Yen",
    "CNY": "Chinese Yuan",
    "AED": "UAE Dirham",
    "SGD": "Singapore Dollar"
}

def get_exchange_rate(from_curr, to_curr):
    try:
        url = f"https://open.er-api.com/v6/latest/{from_curr}"
        res = requests.get(url, timeout=5).json()
        if res.get("result") == "success":
            return res.get("rates", {}).get(to_curr, 1.0)
    except Exception:
        pass
    return 1.0

@app.route('/')
def index():
    return render_template('index.html', currencies=POPULAR_CURRENCIES)

@app.route('/convert', methods=['POST'])
def handle_convert():
    """Processes form submission and redirects to results page."""
    amount = request.form.get('amount', 1.0, type=float)
    from_curr = request.form.get('from_currency', 'USD')
    to_curr = request.form.get('to_currency', 'INR')
    
    return redirect(url_for('result_page', amount=amount, from_curr=from_curr, to_curr=to_curr))

@app.route('/result')
def result_page():
    """Renders the detailed result dashboard page."""
    amount = request.args.get('amount', 1.0, type=float)
    from_curr = request.args.get('from_curr', 'USD')
    to_curr = request.args.get('to_curr', 'INR')

    rate = get_exchange_rate(from_curr, to_curr)
    converted_total = round(amount * rate, 2)
    inverse_rate = round(1 / rate, 4) if rate else 0

    return render_template(
        'result.html',
        amount=amount,
        from_curr=from_curr,
        to_curr=to_curr,
        rate=round(rate, 4),
        converted_total=converted_total,
        inverse_rate=inverse_rate,
        timestamp=time.strftime("%b %d, %Y - %H:%M UTC")
    )

if __name__ == '__main__':
    app.run(debug=True)