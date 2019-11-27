import models

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict
# playhouse is from peewee

# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
savedcar = Blueprint('savedcars', 'savedcar')


@savedcar.route('/', methods=["GET"])
def get_all_savedcars():
 
    try:
        savedcars = [model_to_dict(savedcar) for savedcar in models.SavedCar.select()]
    
        print(savedcars)
        return jsonify(data=savedcars, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


@savedcar.route('/', methods=["POST"])
def create_savedcars():

    payload = request.get_json()
    print(payload, 'payload')

    payload['owner'] = current_user.id
    savedcar = models.SavedCar.create(**payload)
    savedcar_dict = model_to_dict(savedcar)
    
    return jsonify(data=savedcar_dict, status={"code": 201, "message": "Success"})

@savedcar.route('/<id>/', methods=["GET"])
def get_savedcar(id):

    savedcar = models.SavedCar.get_by_id(id)
   

    return jsonify(data=model_to_dict(savedcar), status={"code": 200, "message": "Success"})

@savedcar.route('/<id>/', methods=["PUT"])
def update_car(id):
    payload = request.get_json()
    print(payload)
    query = models.SavedCar.update(
       make=payload['make'],
       model=payload['model'],
       year=payload['year']  
        ).where(models.SavedCar.event_id==id)
    
    query.execute()

    car = models.SavedCar.get_by_id(id)
    car_dict = model_to_dict(car)

    return jsonify(data=car_dict, status={"code": 200, "message": "resource updated successfully"})


@savedcar.route('/<id>/', methods=["DELETE"])
def delete_savedcar(id):
    query = models.SavedCar.delete().where(models.SavedCar.event_id==id)
    query.execute()

    return jsonify(data="this is deleted", status={"code": 200, "message": "resource deleted successfully"}) 