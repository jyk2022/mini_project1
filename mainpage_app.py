from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:amusement@cluster0.ixp01os.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.amusementPark

@app.route('/')
def home():
    return render_template("mainpage_index.html")
# jwt토큰 알아보기






