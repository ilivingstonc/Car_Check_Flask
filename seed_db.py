import models
import json

def seed_database():
    with open('./car_data/honda-crv-2011.json', 'r') a f:
        crv_data = json.reads(f.read())
    

if __name__ == "__main__":
    seed_database()