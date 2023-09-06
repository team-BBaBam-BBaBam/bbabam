from server.app import socketio, app
import logging

if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    # logging.getLogger("openai").setLevel(logging.CRITICAL)

    socketio.run(app, host="0.0.0.0", port=4828, log_output=True, debug=True)
