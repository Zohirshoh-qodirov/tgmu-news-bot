from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'TGMU News Bot is running!'

@app.route('/healthz')
def healthz():
    return 'OK'
