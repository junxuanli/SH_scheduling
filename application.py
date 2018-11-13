from flask import Flask, render_template, request
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