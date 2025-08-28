
# Simple CLI simulator to add parcels and compute routes using the backend models directly.
from backend.models import ParcelStore, simple_route_plan
import random, time, json

def random_point(center=(12.9716, 77.5946), spread_km=5):
    # rough offset in degrees (not geospatially accurate for large spreads)
    return (center[0] + (random.random()-0.5)*0.1, center[1] + (random.random()-0.5)*0.1)

def main():
    store = ParcelStore()
    # create 8 random parcels
    for i in range(8):
        p = {}
        p['pickup_lat'], p['pickup_lng'] = random_point()
        p['dropoff_lat'], p['dropoff_lng'] = random_point()
        p['weight'] = round(random.uniform(0.5, 5.0), 2)
        store.add_parcel(p)
    parcels = store.list_active()
    print('Parcels created:', len(parcels))
    routes = simple_route_plan(parcels, vehicle_count=2, depot=(12.9716,77.5946))
    print(json.dumps(routes, indent=2))

if __name__ == '__main__':
    main()
