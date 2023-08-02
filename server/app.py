from flask import Flask, session, render_template
from flask_socketio import SocketIO, emit, join_room
from flask_session import Session
from bbabam.bbabam import run_bbabam

import random
import string


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)


def generate_random_string(length):
    possible_characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(possible_characters) for _ in range(length))

    return random_string


@app.route("/")
def main():
    return render_template("index.html")


@socketio.on("connect", namespace="/search")
def socket_connect():
    sid = generate_random_string(64)
    session["SESSION_ID"] = sid
    join_room(sid)
    emit("receive_id", sid)


@socketio.on("start", namespace="/search")
def socket_start(data):
    user_input = data["search_text"]
    room_id = data["key"]
    print(user_input)
    if not room_id:
        return emit("error", "Cloud not find SessionId")

    run_bbabam(
        user_input,
        verbose=False,
        socket_module={
            "emit": socketio,
            "app": app,
            "namespace": "/search",
            "room": room_id,
        },
    )


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
