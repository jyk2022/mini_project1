from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient("mongodb+srv://test:sparta@cluster0.ug9qevq.mongodb.net/Cluster0?retryWrites=true&w=majority")
db = client.sparta

@app.route('/')
def home():
   return render_template('introduction.html')

@app.route("/introduction", methods=["POST"])
def introduction_post():
    name_receive = request.form["name_give"]
    comment_receive = request.form["comment_give"]

    doc = {
        'name': name_receive,
        'comment': comment_receive
    }

    db.introduction.insert_one(doc)
    return jsonify({'msg':'댓글 작성 완료!'})

@app.route("/introduction", methods=["GET"])
def introduction_get():
    comment_list = list(db.introduction.find({},{'_id':False}))
    return jsonify({'comments':comment_list})








if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)