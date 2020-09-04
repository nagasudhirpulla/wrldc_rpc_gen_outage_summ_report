from src.config.appConfig import getConfig
from flask import Flask, request, jsonify, render_template
from src.fetchers.outagesFetcher import fetchGenUnitOutagesForWindow
import datetime as dt
# from waitress import serve

app = Flask(__name__)

# get application config
appConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']
reportsConStr: str = appConfig['reportsConStr']


@app.route('/', methods=['POST', 'GET'])
def rpcGenHrs():
    if request.method == 'POST':
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        return render_template('home.html.j2', data={'startDate': startDate, 'endDate': endDate})
    return render_template('home.html.j2')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(appConfig['flaskPort']), debug=True)
    # serve(app, host='0.0.0.0', port=int(appConfig['flaskPort']), threads=1)
