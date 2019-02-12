from flask import Flask, request
from converter import convert_to_all, convert_between

app = Flask(__name__)

@app.route('/convert', methods=['GET'])
def get():
    amount = request.args.get('amount', type=float)
    input_currency = request.args.get('input_currency')
    output_currency = request.args.get('output_currency', default=None)

    if output_currency is None:
        return convert_to_all(amount, input_currency)
    else:
        return convert_between(amount, input_currency, output_currency)

if __name__ == '__main__':
    app.run()
