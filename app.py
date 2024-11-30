from flask import Flask, render_template
from methods.matches import matches_by_date as tday
from methods.db.db import DB

app = Flask(__name__)

@app.route('/')
def hello_world():
    listMatches = tday.getMatchToday()

    return render_template('matches.html', matches=listMatches)
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

