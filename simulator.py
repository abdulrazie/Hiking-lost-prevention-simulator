import random
import time
import math

step_count = 0

leader = {
    "name": "Razie",
    "latitude": 3.14000,
    "longitude": 101.69000,
    "heading": (random.uniform(0, 360))  

}

hiker = {
    "name": "Benjamin",
    "latitude": 3.13990,
    "longitude": 101.68990,
    "heading": (random.uniform(0, 360))
}

def get_distance_meters(lat1, lon1, lat2, lon2):
    # Earth's radius in metres
    R = 6371000.0 
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # Haversine formula
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def move(entity, dt=2.0, speed_mps=1.3):
    # gradually turn instead of jumping to a random new heading
    entity["heading"] += random.uniform(-15, 15)  # degrees turn per step
    heading_rad = math.radians(entity["heading"])
    
    dist_m = speed_mps * dt  # meters this step
    
    # convert meters -> lat/lon deltas
    dlat = (dist_m * math.cos(heading_rad)) / 111320.0
    dlon = (dist_m * math.sin(heading_rad)) / (111320.0 * math.cos(math.radians(entity["latitude"])))
    
    entity["latitude"] += dlat
    entity["longitude"] += dlon



print("Leader")
print(leader["name"])
print(leader["latitude"])
print(leader["longitude"])

print()
print("Hiker")
print(hiker["name"])
print(hiker["latitude"])
print(hiker["longitude"])
print()
print("Simulating walking.. press Ctrl+C to stop")
try:
    while True:
        step_count += 1
        
        move(leader)
        move(hiker)

        distance = get_distance_meters(leader["latitude"], leader["longitude"], hiker["latitude"], hiker["longitude"])
        
        print(f"Step {step_count} | Latitude: {hiker['latitude']:.6f} | Longitude: {hiker['longitude']:.6f} | Distance from leader: {distance:.2f} meters")

        if distance > 50:
            print(f"  WARNING: {hiker['name']} is {distance:.1f}m from {leader['name']}!")

        time.sleep(2)  


except KeyboardInterrupt:
    print("\nSimulation stopped by user.")