from src.config.appConfig import getConfig
from flask import Flask, request, jsonify, render_template
from src.app.rpcGenOutageHrsGenerator import RpcGenOutageHrsGenerator
import datetime as dt
from waitress import serve

app = Flask(__name__)

# get application config
appConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']
reportsConStr: str = appConfig['reportsConStr']


@app.route('/', methods=['POST', 'GET'])
def rpcGenHrs():
    if request.method == 'POST':
        startDate = dt.datetime.strptime(request.form['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(request.form['endDate'], '%Y-%m-%d')
        # make end date time as 23:59:59
        endDate = endDate.replace(
                hour=23, minute=59, second=59, microsecond=0)
        outagesInfoGenerator = RpcGenOutageHrsGenerator(reportsConStr)
        outageHrsInfo = outagesInfoGenerator.getGenOutageHrs(
            startDate, endDate).reset_index(level=0).fillna(0).rename(
                columns={"CAPACITY": "Installed_Cap", 'ELEMENT_NAME': 'Generator'})
        reqGenNames = ("CGPL", "GADARWARA", "JPL", "Jhabua Power", "KAWAS", "KSTPS", "Khargone",
                       "MB Power", "Mouda", "SIPAT", "Sasan", "VSTPS", "Gandhar", "Solapur", "Lara")
        outageHrsInfo = outageHrsInfo[outageHrsInfo.apply(
            lambda x: x['Generator'].startswith(reqGenNames), axis=1)]
        outageHrsInfo = outageHrsInfo.to_dict('records')
        return render_template('home.html.j2', data={'startDate': startDate, 'endDate': endDate, 'outages': outageHrsInfo})
    return render_template('home.html.j2')


if __name__ == '__main__':
    serverMode: str = appConfig['mode']
    if serverMode.lower() == 'd':
        app.run(host="0.0.0.0", port=int(appConfig['flaskPort']), debug=True)
    else:
        serve(app, host='0.0.0.0', port=int(appConfig['flaskPort']), threads=1)
