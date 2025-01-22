from flask import Blueprint, render_template, request, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        symbol = data['symbol'].upper()
        entry_price = float(data['entryPrice'])
        exit_price = float(data['exitPrice'])
        calc_type = data['calcType']
        
        if exit_price >= entry_price:
            return jsonify({
                'error': 'Stop loss should be below entry price for a long position.'
            }), 400
            
        risk_per_share = entry_price - exit_price
        
        if calc_type == '1':  # Portfolio Risk %
            portfolio_size = float(data['portfolioSize'])
            risk_percentage = float(data['riskPercentage'])
            
            if risk_percentage <= 0 or risk_percentage > 100:
                return jsonify({
                    'error': 'Please enter a valid risk percentage between 0 and 100.'
                }), 400
                
            risk_amount = portfolio_size * (risk_percentage / 100)
            shares = int(risk_amount / risk_per_share)
            total_cost = shares * entry_price
            
        else:  # Fixed Dollar Amount
            dollar_amount = float(data['dollarAmount'])
            shares = int(dollar_amount / entry_price)
            total_cost = shares * entry_price
            risk_amount = shares * risk_per_share
            risk_percentage = (risk_amount / dollar_amount) * 100
            
        return jsonify({
            'symbol': symbol,
            'entryPrice': round(entry_price, 2),
            'stopLoss': round(exit_price, 2),
            'riskPerShare': round(risk_per_share, 2),
            'shares': shares,
            'totalCost': round(total_cost, 2),
            'riskAmount': round(risk_amount, 2),
            'riskPercentage': round(risk_percentage, 2)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400