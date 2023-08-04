from flask import Flask, session, render_template, request
from flask_socketio import SocketIO, emit, join_room, disconnect
from bbabam.bbabam import run_bbabam
from flask_cors import CORS

import random
import string


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["SESSION_PERMANENT"] = False
app.config["CORS_HEADERS"] = "Content-Type"

cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


def generate_random_string(length):
    possible_characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(possible_characters) for _ in range(length))

    return random_string


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/status")
def status():
    return "Good!"



@socketio.on("start", namespace="/search")
def socket_start(data):
    user_input = data["search_text"]
    print(user_input)
    room_id = request.sid
    # join_room(room_id)
    print(room_id)
    emit("start_crawling", "Hi!!", room = room_id, namespace="/search")
    emit("start_crawling", "Hi2!!", namespace="/search")
    emit("start_crawling", "Hi3!!")
    if not room_id or room_id == "":
        return emit("error", "Cloud not find SessionId")
    try:
        run_bbabam(
            user_input,
            verbose=False,
            socket_module={
                "emit": socketio,
                "app": app,
                "namespace": "/search",
                "room": room_id
            },
        )
    except Exception as error:
        return emit("error", str(error))


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
