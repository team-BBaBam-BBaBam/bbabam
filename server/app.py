from flask import Flask, session, render_template
from flask_socketio import SocketIO, emit, join_room
from flask_session import Session
from bbabam.bbabam import run_bbabam

import random
import string


# from ..bbabam.bbabam import run_bbabam

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)


@app.route("/")
def main():
    return render_template("index.html")


@socketio.on("start", namespace="/search")
def socket_start(user_input: str):
    print(user_input)
    if session.get("REQUEST_NUM"):
        session["REQUEST_NUM"] += 1
        if session["REQUEST_NUM"] > 3:
            return 0
        run_bbabam(user_input, verbose=False, socket_module=socketio)
    else:
        session["REQUEST_NUM"] = 0
        run_bbabam(
            user_input,
            verbose=False,
            socket_module={
                "emit": socketio,
                "app": app,
                "namespace": "/search",
            },
        )


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=80, debug=True)
