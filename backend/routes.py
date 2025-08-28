
from flask import Blueprint, jsonify, request
from models import ParcelStore, simple_route_plan

router = Blueprint('router', __name__)
store = ParcelStore()

@router.route('/parcels', methods=['GET'])
def list_parcels():
    return jsonify(store.list_parcels())

@router.route('/parcels', methods=['POST'])
def create_parcel():
    data = request.json
    parcel = store.add_parcel(data)
    return jsonify(parcel), 201

@router.route('/pickup', methods=['POST'])
def request_pickup():
    data = request.json or {}
    # Accept optional 'vehicle_count'
    vehicle_count = int(data.get('vehicle_count', 1))
    routes = simple_route_plan(store.list_active(), vehicle_count=vehicle_count)
    return jsonify({"routes": routes})
