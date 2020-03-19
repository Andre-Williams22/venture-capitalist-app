from flask import Flask, render_template

app = Flask(__name__)
# to keep clientside sessions secure 
app.secret_key = 'replace later'

@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)