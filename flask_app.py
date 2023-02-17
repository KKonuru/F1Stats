from flask import Flask, render_template
import f1Info

app = Flask(__name__, template_folder='templates')

@app.route('/')
def hello():
    driversNameList = f1Info.getDrivers()
    return render_template('Home.html',value=driversNameList)

if __name__ == '__main__':
    app.run()
