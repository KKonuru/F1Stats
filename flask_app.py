from flask import Flask, render_template,url_for
import f1Info

app = Flask(__name__, template_folder='templates')
app.config['STATIC_FOLDER'] = 'static'

@app.route('/')
def hello():
    driversNameList = f1Info.getDrivers()
    driverImages = f1Info.getImages()
    return render_template('Home.html',value=driversNameList,images=driverImages)
@app.route('/driver/<name>')
def driver(name):
    return render_template('driver.html',driver=name)

if __name__ == '__main__':
    app.run()
