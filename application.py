from flask import Flask, render_template, request
from io import StringIO
from datetime import datetime
import scheduling_WeekdayDuration
app = Flask(__name__)

#index page
@app.route('/')
def index():
    return render_template('index.html')

#api
@app.route('/scheduler', methods=['POST'])
def scheduler():
    dt_str = request.form['dt']
    dt = datetime.strptime(dt_str, '%m/%d/%Y %I:%M')
    csv = StringIO(request.form['csv'])
    if csv:
        # return scheduling.main(csv)
        return scheduling_WeekdayDuration.main(csv, dt)
    return 'error'

if __name__ == "__main__":
    app.run()