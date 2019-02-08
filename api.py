from flask import Flask, request
from converter import convert

app = Flask(__name__)

@app.route('/convert', methods=['GET'])
def get():
    # Creates arguments
    amount = request.args.get('amount', type=float)
    input_currency = request.args.get('input_currency')
    output_currency = request.args.get('output_currency', default=None)

    # Returns convert function from converter.py
    return convert(amount, input_currency, output_currency)

if __name__ == '__main__':
    app.run(debug=True)
