import models

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict
# playhouse is from peewee

# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
car = Blueprint('cars', 'car')


@car.route('/', methods=["GET"])
def get_all_cars():
 
    all_cars = [model_to_dict(car, max_depth=0) for car in models.Dog.select()]

    return jsonify(data=all_cars, status={'code': 200, 'message': 'Success'})


@car.route('/<car_id>', methods=["GET"])
def get_car(id):
    try: 
        car = model_to_dict(models.Car.get_by_id(id=car_id, max_depth=0))
        return jsonify(data=car, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        # If the id does not match an id of a car in the database return 404 error
        return jsonify(data={}, status={'code': 404, 'message': 'Car not found'})
    
   

@car.route('/', methods=["POST"])
def create_cars():

    payload = request.get_json()
    print(payload, 'payload')
    car = models.Car.create(**payload)

    car_dict = model_to_dict(car)
    
    return jsonify(data=car_dict, status={"code": 201, "message": "Success"})

@car.route('/search', methods=['GET'])
def car_search():
    # Pull make, model and year from query string
    car_make = request.args.get('make')
    car_model = request.args.get('model')
    try:
        # Reject if year is not an integer
        car_year = int(request.args.get('year'))
    except:
        return jsonify(status=400)

    print('Car Make:', car_make)
    # Find results that match query
    results = models.Car.select().where(
        (models.Car.make ** car_make) & (models.Car.model ** car_model) & (models.Car.year == car_year))


    # [model_to_dict(car) for car in results] => would return all 
    
    
    car_dict = model_to_dict(results[0]) # Return first car
    return jsonify(data=car_dict, status={'code': '200', 'msg': 'Search success'})



@car.route('/<id>/', methods=["PUT"])
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


