from flask import Flask, render_template, request, jsonify
from calculator import CarbonCalculator

app = Flask(__name__)
calculator = CarbonCalculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        result = calculator.calculate(data)
        
        # Add personalized recommendations based on the result
        recommendations = calculator.get_recommendations(result['total'])
        result['recommendations'] = recommendations
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/result')
def result_page():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
