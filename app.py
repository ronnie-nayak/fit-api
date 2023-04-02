import time
import cv2 
from flask import Flask, render_template, Response
import mediapipe as mp
import numpy as np
 
from project import exerciseAI, yogaAI  

#-----------------Routing----------------------------------

app = Flask(__name__) 

@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/exercise')
def exercise():   
    return render_template('exercise.html') 
 
@app.route('/yoga')
def yoga():
    return render_template('yoga.html')

@app.route('/yoga/tree')    
def yogaTree():          
    return render_template('yogaTree.html')

@app.route('/about') 
def about(): 
    return render_template('about.html')  


#-----------------Video-Feeds--------------------------------- 
  
@app.route('/bicepCurl_feed')  
def bicepCurl_feed(): 
    return Response(exerciseAI.bicepCurl.gen(), mimetype='multipart/x-mixed-replace; boundary=frame') 
 
@app.route('/tPose_feed') 
def tPose_feed(): 
    return Response(yogaAI.tPose.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')  

@app.route('/treePose_feed')  
def treePose_feed():  
    return Response(yogaAI.treePose.gen() ,mimetype='multipart/x-mixed-replace; boundary=frame')         
 
#--------------------------------------------------------------
app.run(debug=True)