from flask import Flask, render_template
from methods.matches import matches_by_date as tday

app = Flask(__name__)

@app.route('/')
def hello_world():
    listSet = tday.getMatchToday()

    return render_template('matches.html', matches=listSet)

if __name__ == '__main__':
    app.run(debug=True)
