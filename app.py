from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca=certifi.where()

client = MongoClient("mongodb+srv://test:amusement@cluster0.ixp01os.mongodb.net/Cluster0?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.amusementPark

SECRET_KEY = 'SPARTA_3'

import jwt
import datetime
import hashlib

@app.route('/')
def home():
    return render_template("intro.html")

@app.route('/amusementpark')
def main():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template("mainpage_index.html", username= user_info["id"])
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template("mainpage_index.html")

@app.route('/introduction1')
def introduction1():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template("introduction1.html", username=user_info["id"])
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template("introduction1.html")
@app.route('/introduction2')
def introduction2():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template("introduction2.html", username=user_info["id"])
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template("introduction2.html")
@app.route('/introduction3')
def introduction3():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template("introduction3.html", username=user_info["id"])
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template("introduction3.html")

@app.route('/post')
def post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template("post.html", username=user_info["id"])
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template("post.html")

@app.route('/post_up')
def post_up():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template("post_up.html", username=user_info["id"])
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template("post_up.html")

@app.route('/bonuspage')
def bonus():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template("bonuspage.html", username=user_info["id"])
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template("bonuspage.html")


# [회원가입 API]
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'name': name_receive})

    return jsonify({'result': 'success'})

# [로그인 API]
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # .decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# [유저 정보 확인 API]
@app.route('/api/username', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'username': userinfo['name']})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route('/api/register/id_check', methods=['GET'])
def id_check():
    signup_userid_receive = request.args.get('signup_userid_give')
    print(signup_userid_receive)

    result = db.user.find_one({'id': signup_userid_receive})

    if (result == None) :
        return jsonify({'msg': 'ID를 생성할 수 있습니다.', 'status': 'success'})
    else :
        return jsonify({'msg': '중복된 ID가 있습니다.', 'status': 'fail'})

@app.route("/post_up", methods=["POST"])
def web_post_up():
    park_receive = request.form['park_give']
    write_title_receive = request.form['write_title_give']
    name_receive = request.form['name_give']
    ride_receive = request.form['ride_give']
    img_receive = request.form['img_give']
    post_up_list = list(db.post_up.find({}, {'_id': False}))
    count = len(post_up_list) + 1

    doc = {
        'park': park_receive,
        'write_title': write_title_receive,
        'name': name_receive,
        'ride': ride_receive,
        'img': img_receive,
        'like': 0,
        'num': count
    }
    db.post_up.insert_one(doc)
    return jsonify({'msg': '후기 작성 완료!'})

@app.route("/post/post_show", methods=["GET"])
def web_post():
    postUpList = list(db.post_up.find({}, {'_id': False}))
    return jsonify({'postUpLists':postUpList})

#delete 관련 삭제
@app.route("/post/delete", methods=["post"])
def web_post_delet():
    num_receive = request.form['num_give']
    db.post_up.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료하였습니다.!'})

@app.route("/mainpagepost", methods=["GET"])
def mainpage():
    MP_postlist = list(db.post_up.find({}, {'_id': False}))
    return jsonify({'MP_postlists': MP_postlist})


@app.route("/introduction_post", methods=["POST"])
def introduction_post():
    name_receive = request.form["name_give"]
    comment_receive = request.form["comment_give"]

    doc = {
        'name': name_receive,
        'comment': comment_receive
    }

    db.introduction.insert_one(doc)
    return jsonify({'msg':'댓글 작성 완료!'})

@app.route("/introduction_read", methods=["GET"])
def introduction_get():
    comment_list = list(db.introduction.find({},{'_id':False}))
    return jsonify({'comments':comment_list})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)