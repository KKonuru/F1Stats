from flask import Flask, render_template
import f1Info
import flask
from compare_dash import create_dash_app

app = Flask(__name__, template_folder='templates')
app.config['STATIC_FOLDER'] = 'static'
app.config.suppress_callback_exceptions = True



create_dash_app(app)

@app.route('/')
def home():
    driversNameList = f1Info.getDrivers()
    driverImages = f1Info.getImages()
    return render_template('Home.html',value=driversNameList,images=driverImages)

@app.route('/driver/<name>')
def driver(name):
    return render_template('driver.html',driver=name)

if __name__ == '__main__':
    app.run()
