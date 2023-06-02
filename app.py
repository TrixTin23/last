from flask import Flask, render_template, request, session
import matplotlib.pyplot as plt
import requests
import pandas as pd
from flask_ngrok import run_with_ngrok

# membuat nama app
app = Flask(__name__)
app.config['FLASKNGROK_AUTH_TOKEN'] = '2QdgscZzay4kfUMIfCjuEI0I8KP_5d7nqeSgCCnEk2cbm9LaL'
app.secret_key = '2Qe0L2JsvGTk1mVGNokLvRf1v8j_4YSvG723TxcS73PCRTdca'
run_with_ngrok(app)

data = pd.read_excel('predicted_values.xlsx')

# =========================== MEMBACA FILE ===================================
@app.route('/')
def index():
    limited_data = data.head(50)
    table_data1 = limited_data.to_dict(orient='records')
    return render_template('index.html', table_data1=table_data1)

# =========================== TUKAR MATA UANG ===================================
@app.route('/', methods=['POST'])
def convert():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        base_currency = request.form['base_currency']
        target_currency = request.form['target_currency']

        # Mengirim permintaan ke API untuk mendapatkan data kurs mata uang terbaru
        api_url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(api_url)
        data = response.json()
        target_rate = data['rates'][target_currency]

        converted_amount = amount * target_rate

    return render_template('index.html', amount=amount, base_currency=base_currency,
                           target_currency=target_currency, converted_amount=converted_amount)

# =========================== PREDIKSI ===================================
@app.route('/prediksi', methods=['GET', 'POST'])
def prediksi():
    if 'table_data' not in session:
        table_data = data.to_dict(orient='records')
    else:
        table_data = session['table_data']

    return render_template('index.html', table_data=table_data)

# # =========================== FILTER ===================================
@app.route('/filter', methods=['GET', 'POST'])
def filter_data():
    # Get the month and year values from the form
    month = int(request.form['month'])
    year = int(request.form['year'])

    filtered_data = data[(data['Date'].dt.month == month) & (data['Date'].dt.year == year)]

    table_data = filtered_data.to_html(index=False, classes='data')
    session['table_data'] = table_data

    return render_template('index.html', table_data=table_data)

# =========================== MENJALANKAN APP ===================================
if __name__ == '__main__':
	app.run()