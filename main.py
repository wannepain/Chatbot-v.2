from flask import Flask, json, jsonify
from flask import request
from flask_cors import CORS, cross_origin
import os


# app config
app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"

cors = CORS(app)


@app.route("/")
def respond_test():
    return jsonify({"hello": "world"})


# @app.route("/respond", methods=["POST"])
# @cross_origin()
# def respond_route():  # need to move the used question idx to the global scope
#     request_data = request.get_json()
#     history_in_req = request_data["history"]
#     used_question_idx = request_data["used_question_idx"]

#     respond(history_in_req, corpus, used_question_idx, nlp=get_nlp())

#     return jsonify(
#         {
#             "history": history_in_req,
#             "used_question_idx": used_question_idx,
#         }
#     )


# @app.route("/career", methods=["POST"])
# @cross_origin()
# def career_route():
#     request_data = request.get_json()
#     history_in_req = request_data["history"]
#     career = return_career(history_in_req, get_nlp())
#     return jsonify({"career": career})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(
        host="0.0.0.0",
        port=port,
    )
