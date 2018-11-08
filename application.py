from flask import Flask, url_for, render_template, request
from io import StringIO
import scheduling
app = Flask(__name__)

#index page
@app.route('/')
def index():
    return render_template('index.html')

#api
@app.route('/scheduler', methods=['POST'])
def scheduler():
    csv = StringIO(request.form['csv'])
    if csv:
        return scheduling.main(csv)
    return 'error'

if __name__ == "__main__":
    app.run()
    url_for('static', filename='logo.svg')
    url_for('static', filename='bootstrap-4.1.3.min.css')
    url_for('static', filename='style.css')
    url_for('static', filename='jquery-3.3.1.min.js')
    url_for('static', filename='bootstrap-4.1.3.min.js')
    url_for('static', filename='main.js')