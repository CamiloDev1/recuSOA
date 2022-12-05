from email import message
from flask import Flask, Response, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId, json_util
from pymongo import MongoClient
app = Flask(__name__)

app.config['MONGO_URI']='mongodb+srv://camilo:08diciembre@cluster0.m0efscn.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient("mongodb+srv://camilo:08diciembre@cluster0.m0efscn.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('ejemplo')
records = db.tasks

mongo=PyMongo(app)

@app.route('/ejemplo',methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']
    if title and description:
        id = records.insert_one({
            'title': title, 'description': description
        })
        response= {
            'id':str(id),
            'title': title, 'description': description
        }
        return response
    
    else:
        return notFound()

@app.route('/ejemplo',methods=['GET'])
def get_tasks():
    tasks = records.find()
    response = json_util.dumps(tasks)
    return Response(response,mimetype='application/json')

@app.route('/ejemplo/<id>',methods=['GET'])
def get_task(id):
    task = records.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(task)
    return Response(response,mimetype='application/json')

@app.route('/ejemplo/<id>',methods=['DELETE'])
def delete_task(id):
    task = records.delete_one({'_id': ObjectId(id)})
    response = {'message': 'user '+id+' deleted'}
    return response

@app.route('/ejemplo/<id>',methods=['PUT'])
def update_task(id):

    title = request.json['title']
    description = request.json['description']
    if title and description:
        task = records.update_one({'_id': ObjectId(id)}, { '$set':{
            'title': title, 'description': description
        }})
        response = {'message': 'user '+id+' updated'}
        return response
@app.errorhandler(404)
def notFound(error=None):
    response = jsonify({'message': 'resurce not found '+request.url,
    'status': 404})
    response.status_code=404

    return response

if __name__ == "__main__":
    app.run(debug=True)