import time
import cv2
from flask import Flask, render_template, Response
import mediapipe as mp
import numpy as np

from project import exerciseAI, yogaAI

# -----------------Routing----------------------------------

app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/exercise/biceps-curl')
@app.route("/")
def exerciseBicepsCurl():
    return render_template("exerciseBicepsCurl.html")


@app.route("/exercise/push-ups")
def exercisePushUps():
    return render_template("exercisePushUps.html")


@app.route("/exercise/triceps")
def exerciseTriceps():
    return render_template("exerciseTriceps.html")


@app.route("/exercise/squats")
def exerciseSquats():
    return render_template("exerciseSquats.html")


@app.route("/yoga/t-pose")
def yogaT():
    return render_template("yogaT.html")


@app.route("/yoga/tree-pose")
def yogaTree():
    return render_template("yogaTree.html")


@app.route("/yoga/warrior-pose")
def yogaWarrior():
    return render_template("yogaWarrior.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/bmi")
def bmi():
    return render_template("bmi.html")


# -----------------Video-Feeds---------------------------------


@app.route("/bicepCurl_feed")
def bicepCurl_feed():
    return Response(
        exerciseAI.bicepCurl.gen(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/pushUps_feed")
def pushUps_feed():
    return Response(
        exerciseAI.pushUps.gen(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/triceps_feed")
def triceps_feed():
    return Response(
        exerciseAI.triceps.gen(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/squats_feed")
def squats_feed():
    return Response(
        exerciseAI.squats.gen(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/tPose_feed")
def tPose_feed():
    return Response(
        yogaAI.tPose.gen(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/treePose_feed")
def treePose_feed():
    return Response(
        yogaAI.treePose.gen(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/warriorPose_feed")
def warriorPose_feed():
    return Response(
        yogaAI.warriorPose.gen(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# --------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

