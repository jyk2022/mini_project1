from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:amusement@cluster0.ixp01os.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.amusementPark

# post 관련 api

@app.route('/')
def post():
    return render_template('post.html')

@app.route('/post_up')
def post_up():
    return render_template('post_up.html')

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

@app.route("/post", methods=["GET"])
def web_post():
    postUpList = list(db.post_up.find({}, {'_id': False}))
    return jsonify({'postUpLists':postUpList})


# @app.route('/post/like', methods=['POST'])
# def post_like():
#     id_receive = request.form['id_give']
#     like_star = db.post_up.find_one({'id': id_receive})
#     current_like = like_star['like']
#
#     new_like = current_like + 1
#
#     db.post_up.update_one({'idd': i_receive}, {'$set': {'like': new_like}})
#
#     return jsonify({'msg': '좋아요 완료!'})

#delete 관련 삭제

@app.route("/post/delete", methods=["post"])
def web_post_delet():
    num_receive = request.form['num_give']
    db.post_up.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료하였습니다.!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)