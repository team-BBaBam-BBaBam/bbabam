from flask import Flask, session, render_template, request
from flask_socketio import SocketIO, emit, join_room, disconnect
from bbabam.bbabam import run_bbabam
from flask_cors import CORS
import json
from random import choices
from bbabam.settings.errors import (
    ChatExceptionError,
    WrongAccessError,
)


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["CORS_HEADERS"] = "Content-Type"

cors = CORS(app)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading",
    logger=True,
    # engineio_logger=True,
)

with open("server/picture.json", "r") as file:
    picture_dataset = json.load(file)

with open("server/korean_to_english_dict.json", "r") as file:
    korean_to_english = json.load(file)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/status")
def status():
    return "Good!"


@app.route("/loadimage/<num>", methods=["GET"])
def get_picture(num):
    num = min(int(num), 20)
    res = []
    index = 0
    while True:
        if index == num:
            break
        pic_data = choices(picture_dataset["item"], k=1)
        if pic_data[0]["galTitle"] in korean_to_english:
            res += [
                {
                    "url": pic_data[0]["galWebImageUrl"],
                    "korean_title": pic_data[0]["galTitle"],
                    "english_title": korean_to_english[pic_data[0]["galTitle"]],
                    "create_time": pic_data[0]["galCreatedtime"],
                    "modified_time": pic_data[0]["galModifiedtime"],
                    "month": pic_data[0]["galPhotographyMonth"],
                    "location": pic_data[0]["galPhotographyLocation"],
                    "keywords": pic_data[0]["galSearchKeyword"].split(", "),
                }
            ]
            index += 1
        else:
            continue

    return json.dumps(res)


@socketio.on("start", namespace="/search")
def socket_start(data):
    user_input = data["search_text"]
    print(user_input)
    room_id = request.sid
    join_room(room_id)
    print(room_id)
    if not room_id or room_id == "":
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
    # except ChatExceptionError as error:
    #     print("error code 1", error)
    #     emit(
    #         "error",
    #         {"err_code": 1, "err_msg": str(error)},
    #         room=room_id,
    #         namespace="/search",
    #     )
    # except Exception as error:
    #     print(error)
    #     emit(
    #         "error",
    #         {"err_code": 0, "err_msg": str(error)},
    #         room=room_id,
    #         namespace="/search",
    #     )


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
