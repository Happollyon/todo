from crypt import methods
import re
from urllib import response
from flask import Flask, jsonify,request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from flask_cors import CORS

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


@app.route('/register/<string:username>/<string:password>',methods=['GET'])
def register(username,password):
    usernamecheck = db.execute("SELECT * FROM users WHERE username = :username ",{'username':username}).fetchall()
    db.commit()
    if usernamecheck:
        response = jsonify({'login':False})
        response.headers.add("Access-Control-Allow-Origin", "*")
        print('success')
        return  response
    else:    
        result = db.execute("INSERT INTO users(username,password) VALUES(:username,:password) RETURNING user_id, username",{'username':username,'password':password}).fetchall()
        db.commit()
        response = jsonify({'login':True,'response':[dict(row) for row in result]})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return  response

@app.route('/login/<string:username>/<string:password>',methods=['GET'])
def login(username,password):
    result = db.execute("SELECT username,user_id FROM users WHERE username=:username AND password =:password",{'username':username,'password':password}).fetchall()
    db.commit()
    if result:
        response = jsonify({'login':True,'response':[dict(row) for row in result]})
        response.headers.add("Access-Control-Allow-Origin", "*")
        print('success')
        return  response
    else:
        response = jsonify({'login':False})
        response.headers.add("Access-Control-Allow-Origin", "*")
        print('success')
        return  response

if __name__ == '__main__':
    app.run(debug=True)