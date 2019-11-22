import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict
# playhouse is from peewee

# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
car = Blueprint('cars', 'car')


@car.route('/', methods=["GET"])
def get_all_cars():
 
    try:
        cars = [model_to_dict(car) for car in models.Car.select()]
    
        print(car)
        return jsonify(data=cars, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


@car.route('/', methods=["POST"])
def create_cars():

    payload = request.get_json()
    print(payload, 'payload')
    car = models.Car.create(**payload)

    car_dict = model_to_dict(car)
    
    return jsonify(data=car_dict, status={"code": 201, "message": "Success"})

@car.route('/<id>', methods=["GET"])
def get_car(id):

    car = models.Car.get_by_id(id)
   

    return jsonify(data=model_to_dict(car), status={"code": 200, "message": "Success"})

@car.route('/<id>', methods=["PUT"])
def update_car(id):
    payload = request.get_json()
    query = models.Car.update(**payload).where(models.Car.id==id)
    query.execute()

    car = models.Car.get_by_id(id)
    car_dict = model_to_dict(car)

    return jsonify(data=car_dict, status={"code": 200, "message": "resource updated successfully"})


@car.route('/<id>', methods=["DELETE"])
def delete_car(id):
    query = models.Car.delete().where(models.Car.id==id)
    query.execute()

    return jsonify(data="this is deleted", status={"code": 200, "message": "resource deleted successfully"})    


