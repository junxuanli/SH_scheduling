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
    return 'error', 500

@app.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    return '500 error', 500
    # return render_template('500.html'), 500

if __name__ == "__main__":
    if app.debug is not True:
        import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('flask.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.run(host='0.0.0.0', port=80)
    # app.run()