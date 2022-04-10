from flask import Flask, request
import toonsun as ts

app = Flask(__name__)

@app.route("/scan", methods=["GET", "POST"])
def scan():
    text = request.args.get("text", None)
    if text is None:
        req = request.get_json()
        text = req.get("text")
    return {"scan": ts.scan(text), "syllable": ts.into_syllables(text)}


@app.route("/scansim", methods=["GET", "POST"])
def scansim():
    req = request.get_json()
    texts = req.get("texts")
    scans = [ts.scan(t) for t in texts]
    return dict(zip(texts, scans))
