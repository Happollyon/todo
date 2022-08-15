from crypt import methods
from dataclasses import dataclass
import re
from sre_constants import SUCCESS
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

#createTable("ALTER TABLE task ADD COLUMN item_id INT NOT NULL")


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

@app.route('/additem/<int:user_id>/<string:title>')
def additem(user_id,title):
    print(user_id, title)
    item_id= db.execute("INSERT INTO item(title,user_id) VALUES(:title,:user_id) ",{'title':title,'user_id':user_id})
    db.commit()
    response = jsonify({'title':title})
    response.headers.add("Access-Control-Allow-Origin", "*")
    print('success adding item')
    return  response
    
@app.route('/selectitems/<int:user_id>')
def selectitems(user_id):
    data = db.execute("SELECT item.item_id,item.title,users.username FROM users INNER JOIN item ON users.user_id=item.user_id where users.user_id=:user_id",   {'user_id':user_id}).fetchall()
    db.commit()
    response = jsonify({'data':[dict(row) for row in data]})
    response.headers.add("Access-Control-Allow-Origin", "*")
    print('success collecting items')
    return  response
@app.route('/addtask/<int:user_id>/<int:item_id>/<string:description>')
def addtask(user_id,item_id,description):
    db.execute("INSERT INTO task(description,item_id) VALUES(:description,:item_id)",{'user_id':user_id,'description':description,'item_id':item_id})
    db.commit()
    print('Task added')
    response = jsonify({'added':True})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True)