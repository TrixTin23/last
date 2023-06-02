from flask import Flask, render_template, request, session
import matplotlib.pyplot as plt
import requests
import pandas as pd
from flask_ngrok import run_with_ngrok

# membuat nama app
app = Flask(__name__)
app.secret_key = '2Ox2BCzXHp8J8hcbwFWtSYF1s05_4YNvFMMrgMZRDWJ1YrSxS'
run_with_ngrok(app)

data = pd.read_excel('predicted_values.xlsx')

# =========================== MEMBACA FILE ===================================
@app.route('/')
def index():
    limited_data = data.head(50)
    table_data1 = limited_data.to_dict(orient='records')
     # Read the Excel file
    # data = pd.read_excel('predicted_values.xlsx')

    # # Limit the data to 100 rows
    # limited_data = data.head(100)

    # table_data = limited_data.to_html(classes='data')

    # # Convert the data to the appropriate format for HTML rendering
    # # table_data = data.to_dict(orient='records')

    # #FILTERING DATA
    # month = request.args.get('month')
    # year = request.args.get('year')

    # if month and year:
    #     filtered_data = data[
    #         (data['Date'].dt.month == int(month)) & (data['Date'].dt.year == int(year))
    #     ]
    # Extract the Date and Predicted USD_IDR Exchange Rate columns
    # dates = limited_data['Date']
    # exchange_rates = limited_data['Exchange rate']

    # # Create a line plot
    # plt.figure(figsize=(10, 6))
    # plt.plot(dates, exchange_rates, color='green', marker='o', linestyle='solid', linewidth=2, markersize=6)
    # plt.xlabel('Date')
    # plt.ylabel('Predicted USD_IDR Exchange Rate')
    # plt.title('Predicted Exchange Rate')
    # plt.xticks(rotation=45)
    # plt.tight_layout()

    # # Save the plot to a file
    # plot_path = 'static/plot.png'
    # plt.savefig(plot_path)
    # plt.close()

    # Render the HTML template and pass the data to the web page
    # return render_template('index.html', table_data=table_data, data=filtered_data.to_html())
    return render_template('index.html', table_data1=table_data1)

# =========================== TUKAR MATA UANG ===================================
@app.route('/konversi', methods=['POST'])
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

# =========================== FILTER ===================================
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
    # Run Flask di localhost 
	app.run()