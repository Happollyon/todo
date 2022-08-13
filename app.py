from shutil import unregister_unpack_format
from sre_constants import SUCCESS
from urllib import request
from flask import Flask, jsonify,request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

app = Flask(__name__)
engine = create_engine("postgresql://ftrxafhanwopfs:4799a0f535c4c402e226523afefbbecfc2f3a3fc85bfce8c3013b9d589758a2d@ec2-52-18-116-67.eu-west-1.compute.amazonaws.com:5432/d1hk19qr73vntu")
db = scoped_session(sessionmaker(bind=engine))
#index page
@app.route('/')
def index():
    return 'todo, Flask!'

#This function is used to create the tables
def createTable(query):
    db.execute(query)
    db.commit()
    print('SUCCESS!')


@app.route('/register', methods = ['POST'])
def register():
    username = request.get_json(force=True)
    print(username['username'])
    return jsonify({'username':username['username']})

if __name__ == '__main__':
    app.run(debug=True)