from flask import Flask, json, jsonify
from flask import request
from flask_cors import CORS, cross_origin
import os
from src.respond import respond
from openai import OpenAI
from src.career import evaluate
from src.compliment import compliment

# from src_limited.chatbot import respond as respond_limited
# from src_limited.corpus import inicialize_medium_corpus  # Corrected import
# from src_limited.career import return_career
# import spacy

# app config
app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"

cors = CORS(app)

client = OpenAI(api_key=os.getenv("OPEN_AI_TOKEN"))

# corpus = inicialize_medium_corpus()


# def get_nlp():
#     if not hasattr(app, "nlp"):
#         app.nlp = spacy.load(
#             "en_core_web_sm", disable=["parser", "ner"]
#         )  # Disabling components saves memory
#     return app.nlp


@app.route("/")
def respond_test():
    return jsonify({"hello": "world"})


@app.route("/respond/unlimited", methods=["POST"])
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


@app.route("/career/unlimited", methods=["POST"])
@cross_origin()
def career_route():
    request_data = request.get_json()
    history_in_req = request_data["history"]
    career = evaluate(history=history_in_req, client=client)
    return jsonify({"career": career})


@app.route("/compliment", methods=["POST"])
@cross_origin()
def compliment_route():
    request_data = request.get_json()
    history_in_req = request_data["history"]
    if history_in_req is None or len(history_in_req) == 0:
        return (
            jsonify(
                {
                    "error": "history is None or empty",
                    "message": None,
                }
            ),
            400,
        )
    result = compliment(history=history_in_req, client=client)
    return jsonify({"compliment": result})


# @app.route("/respond/limited", methods=["POST"])
# @cross_origin()
# def limited_respond():
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


# @app.route("/career/limited", methods=["POST"])
# @cross_origin()
# def limited_career():
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
