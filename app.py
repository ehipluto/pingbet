from flask import Flask, render_template
from methods.matches import matches_by_date as tday

app = Flask(__name__)

@app.route('/')
def hello_world():
    listSet = tday.getMatchToday()

    return render_template('matches.html', matches=listSet)
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')
