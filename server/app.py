#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries=Bakery.query.all()
    response=[bakery.to_dict() for bakery in bakeries]

    return jsonify(response)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery=Bakery.query.filter_by(id=id).first()
    return jsonify({
        "baked_goods":[
            {
                "bakery_id":bk.bakery_id,
                "created_at":bk.created_at.strftime('%Y-%m-%d %H:%M:%S') if bk.created_at else None,
                "id":bk.id,
                "name":bk.name,
                "price":bk.price,
                "updated_at":bk.updated_at.strftime('%Y-%m-%d %H:%M:%S') if bk.updated_at else None
            }
        for bk in bakery.baked_goods],
        "created_at":bakery.created_at.strftime('%Y-%m-%d %H:%M:%S') if bakery.created_at else None,
        "id":bakery.id,
        "name":bakery.name,
        "updated_at":bakery.updated_at.strftime('%Y-%m-%d %H:%M:%S') if bakery.updated_at else None

    })

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    if not baked_goods:
        return jsonify({"error": "No baked goods found"}), 404  
    response = []
    for bg in baked_goods:
        bakery = bg.bakery 
        
        bakery_data = None
        if bakery:
            bakery_data = {
                "id": bakery.id,
                "name": bakery.name,
                "created_at": bakery.created_at.strftime('%Y-%m-%d %H:%M:%S') if bakery.created_at else None,
                "updated_at": bakery.updated_at.strftime('%Y-%m-%d %H:%M:%S') if bakery.updated_at else None
            }

        response.append({
            "id": bg.id,
            "name": bg.name,
            "price": bg.price,
            "bakery_id": bg.bakery_id,
            "created_at": bg.created_at.strftime('%Y-%m-%d %H:%M:%S') if bg.created_at else None,
            "updated_at": bg.updated_at.strftime('%Y-%m-%d %H:%M:%S') if bg.updated_at else None,
            "bakery": bakery_data  # Include bakery data or None if no bakery found
        })

    return jsonify(response)


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good= BakedGood.query.order_by(BakedGood.price.desc()).first()

    bakery_data = None
    if baked_good.bakery:  # Check if bakery exists before accessing its attributes
        bakery_data = {
            "id": baked_good.bakery.id,
            "name": baked_good.bakery.name,
            "created_at": baked_good.bakery.created_at.strftime("%Y-%m-%d %H:%M:%S") if baked_good.bakery.created_at else None,
            "updated_at": baked_good.bakery.updated_at.strftime("%Y-%m-%d %H:%M:%S") if baked_good.bakery.updated_at else None,
        }

    # Manually construct the dictionary
    baked_good_dict = {
        "id": baked_good.id,
        "name": baked_good.name,
        "price": baked_good.price,
        "created_at": baked_good.created_at.strftime("%Y-%m-%d %H:%M:%S") if baked_good.created_at else None,
        "updated_at": baked_good.updated_at.strftime("%Y-%m-%d %H:%M:%S") if baked_good.updated_at else None,
        "bakery_id": baked_good.bakery_id,
        "bakery": bakery_data  # Set to None if no bakery exists
    }

    return jsonify(baked_good_dict)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
