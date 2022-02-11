from flask import Flask, request, Response, redirect, send_file, render_template                                                     
import threading

data = 'foo'
host_name = "0.0.0.0"
port = 23336
app = Flask(__name__)

def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route("/shutdown")
def shutdown():
    shutdown()

@app.route("/")
def main():
    return data

threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=True, use_reloader=False)).start()