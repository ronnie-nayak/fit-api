import time
import cv2 
from flask import Flask, render_template, Response
import mediapipe as mp  
import numpy as np 


from .bicepCurl import * 
from .pushUps import *   
from .triceps import * 
from .squats import * 
from ..exerciseAI.util import *    
