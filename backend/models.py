
import math, uuid, time
from copy import deepcopy

class ParcelStore:
    def __init__(self):
        self.parcels = {}  # id -> parcel dict

    def add_parcel(self, data):
        # expected fields: pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, weight(optional)
        pid = str(uuid.uuid4())[:8]
        parcel = {
            "id": pid,
            "created_at": time.time(),
            "pickup_lat": float(data.get('pickup_lat', 0)),
            "pickup_lng": float(data.get('pickup_lng', 0)),
            "dropoff_lat": float(data.get('dropoff_lat', 0)),
            "dropoff_lng": float(data.get('dropoff_lng', 0)),
            "weight": float(data.get('weight', 1.0)),
            "status": "waiting"
        }
        self.parcels[pid] = parcel
        return deepcopy(parcel)

    def list_parcels(self):
        return [deepcopy(p) for p in self.parcels.values()]

    def list_active(self):
        # active means waiting pickups
        return [p for p in self.parcels.values() if p['status'] == 'waiting']

def haversine(a_lat, a_lng, b_lat, b_lng):
    # returns approximate kilometers between two lat/lng points
    R = 6371.0
    from math import radians, sin, cos, asin, sqrt
    dlat = radians(b_lat - a_lat)
    dlng = radians(b_lng - a_lng)
    a = sin(dlat/2)**2 + cos(radians(a_lat))*cos(radians(b_lat))*sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def simple_route_plan(parcels, vehicle_count=1, depot=(0.0,0.0)):
    "
    Very small nearest-neighbor greedy partitioning for demo:
    - Assign parcels to vehicles by nearest pickup to current vehicle position.
    - Each vehicle starts at depot.
    Returns list of routes where each route is list of parcel IDs in pickup order.
    "
    if not parcels:
        return []
    parcels_copy = parcels.copy()
    # represent parcels as dict with coords
    remaining = {p['id']: p for p in parcels_copy}
    vehicles = [{"pos": depot, "route": []} for _ in range(max(1, vehicle_count))]
    while remaining:
        for v in vehicles:
            if not remaining:
                break
            # find nearest parcel pickup to v['pos']
            best_id = None
            best_dist = None
            for pid, p in remaining.items():
                d = haversine(v['pos'][0], v['pos'][1], p['pickup_lat'], p['pickup_lng'])
                if best_dist is None or d < best_dist:
                    best_dist = d
                    best_id = pid
            # assign best_id to vehicle
            v['route'].append(best_id)
            # move vehicle to that parcel's dropoff (simulate)
            target = remaining[best_id]
            v['pos'] = (target['dropoff_lat'], target['dropoff_lng'])
            del remaining[best_id]
    # return only route lists
    return [v['route'] for v in vehicles]
