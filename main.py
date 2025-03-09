from flask import Flask, json, jsonify
from flask import request
from flask_cors import CORS, cross_origin
import os
from src.respond import respond
from openai import OpenAI
from src.career import evaluate

# app config
app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"

cors = CORS(app)

client = OpenAI(api_key=os.getenv("OPEN_AI_TOKEN"))


@app.route("/")
def respond_test():
    return jsonify({"hello": "world"})


@app.route("/respond", methods=["POST"])
@cross_origin()
def respond_route():  # need to move the used question idx to the global scope
    request_data = request.get_json()
    history_in_req = request_data["history"]

    history = respond(history=history_in_req, client=client)

    return jsonify(
        {
            "history": history,
        }
    )


@app.route("/career", methods=["POST"])
@cross_origin()
def career_route():
    request_data = request.get_json()
    history_in_req = request_data["history"]
    career = evaluate(history=history_in_req, client=client)
    return jsonify({"career": career})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(
        host="0.0.0.0",
        port=port,
    )
