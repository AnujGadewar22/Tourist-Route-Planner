'''
import itertools
import math

# Step 1: Calculate Distance Using Haversine Formula
def calculate_distance(coord1, coord2):
    R = 6371  # Radius of Earth in kilometers
    lat1, lon1 = coord1  # Unpack latitude and longitude
    lat2, lon2 = coord2
    
    # Convert degrees to radians
    lat1, lon1 = math.radians(lat1), math.radians(lon1)
    lat2, lon2 = math.radians(lat2), math.radians(lon2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in kilometers

# Step 2: Create Distance Matrix
def create_distance_matrix(locations):
    n = len(locations)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = calculate_distance(locations[i]['coords'], locations[j]['coords'])
    return matrix

# Step 3: Solve TSP Using Brute Force
def solve_tsp(distance_matrix, start=0):
    n = len(distance_matrix)
    vertices = list(range(n))
    vertices.remove(start)
    
    min_path = float('inf')
    best_route = []
    
    for perm in itertools.permutations(vertices):
        current_path_weight = 0
        k = start
        for j in perm:
            current_path_weight += distance_matrix[k][j]
            k = j
        current_path_weight += distance_matrix[k][start]  # Return to start
        
        if current_path_weight < min_path:
            min_path = current_path_weight
            best_route = [start] + list(perm) + [start]
    
    return best_route, min_path

# Predefined Tourist Places in Pune with Coordinates
tourist_places = {
    "shaniwar wada": (18.5185, 73.8554),
    "aga khan palace": (18.5523, 73.9024),
    "sinhagad fort": (18.3662, 73.7550),
    "dagadusheth halwai ganapati temple": (18.5147, 73.8553),
    "pataleshwar cave temple": (18.5203, 73.8490),
    "pashan lake": (18.5408, 73.7803),
    "rajiv gandhi zoological park": (18.4497, 73.8656),
    "parvati hill": (18.5019, 73.8521),
    "osho international meditation resort": (18.5362, 73.9031),
    "raja dinkar kelkar museum": (18.5102, 73.8544),
    "empress garden": (18.5123, 73.8860),
    "national war memorial southern command": (18.5181, 73.8918),
    "baner hill": (18.5472, 73.7948),
    "mulshi dam": (18.4833, 73.4079),
    "khadakwasla dam": (18.4247, 73.7659),
    "chaturshringi temple": (18.5329, 73.8283),
    "vetal tekdi": (18.5292, 73.8062),
    "fergusson college road": (18.5174, 73.8400),
    "pune-okayama friendship garden": (18.4818, 73.8348),
    "bund garden": (18.5390, 73.8902)
}

# Main Function
if __name__ == "__main__":
    print("Welcome to the Pune Tourist Route Planner!")
    n = int(input("Enter the number of tourist places you want to visit: "))
    
    locations = []
    for i in range(n):
        place = input(f"Enter the name of tourist place {i + 1}: ").strip().lower()
        if place in tourist_places:
            locations.append({"name": place.title(), "coords": tourist_places[place]})
        else:
            print(f"Error: {place.title()} is not available in our database. Please try again.")
            exit()

    # Generate Distance Matrix
    distance_matrix = create_distance_matrix(locations)
    
    # Solve TSP
    start_point = 0  # Start from the first place entered
    route, min_distance = solve_tsp(distance_matrix, start=start_point)
    
    # Output Results
    print("\nOptimized Route (Indices):", route)
    print("Minimum Distance:", round(min_distance, 2), "km")
    
    # Map Route Indices to Names
    route_names = [locations[i]['name'] for i in route]
    print("Optimized Route (Names):", " -> ".join(route_names))


'''

from flask import Flask, render_template, request, jsonify
import itertools
import math

app = Flask(__name__)



# Predefined Tourist Spots
tourist_places = {
    "shaniwar wada": (18.5185, 73.8554),
    "aga khan palace": (18.5523, 73.9024),
    "sinhagad fort": (18.3662, 73.7550),
    "dagadusheth halwai ganapati temple": (18.5147, 73.8553),
    "pataleshwar cave temple": (18.5203, 73.8490),
    "pashan lake": (18.5408, 73.7803),
    "rajiv gandhi zoological park": (18.4497, 73.8656),
    "parvati hill": (18.5019, 73.8521),
    "osho international meditation resort": (18.5362, 73.9031),
    "raja dinkar kelkar museum": (18.5102, 73.8544),
    "empress garden": (18.5123, 73.8860),
    "national war memorial southern command": (18.5181, 73.8918),
    "baner hill": (18.5472, 73.7948),
    "mulshi dam": (18.4833, 73.4079),
    "khadakwasla dam": (18.4247, 73.7659),
    "chaturshringi temple": (18.5329, 73.8283),
    "vetal tekdi": (18.5292, 73.8062),
    "fergusson college road": (18.5174, 73.8400),
    "pune-okayama friendship garden": (18.4818, 73.8348),
    "bund garden": (18.5390, 73.8902)
}

# Helper functions (calculate_distance, create_distance_matrix, solve_tsp) from your code
def calculate_distance(coord1, coord2):
    R = 6371  # Radius of Earth in kilometers
    lat1, lon1 = coord1  # Unpack latitude and longitude
    lat2, lon2 = coord2
    
    # Convert degrees to radians
    lat1, lon1 = math.radians(lat1), math.radians(lon1)
    lat2, lon2 = math.radians(lat2), math.radians(lon2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in kilometers

# Step 2: Create Distance Matrix
def create_distance_matrix(locations):
    n = len(locations)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = calculate_distance(locations[i]['coords'], locations[j]['coords'])
    return matrix
def solve_tsp(distance_matrix, start=0):
    n = len(distance_matrix)
    vertices = list(range(n))
    vertices.remove(start)
    
    min_path = float('inf')
    best_route = []
    
    for perm in itertools.permutations(vertices):
        current_path_weight = 0
        k = start
        for j in perm:
            current_path_weight += distance_matrix[k][j]
            k = j
        current_path_weight += distance_matrix[k][start]  # Return to start
        
        if current_path_weight < min_path:
            min_path = current_path_weight
            best_route = [start] + list(perm) + [start]
    
    return best_route, min_path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    spots = request.json.get("spots", [])
    locations = [{"name": spot.title(), "coords": tourist_places[spot.lower()]} for spot in spots if spot.lower() in tourist_places]
    distance_matrix = create_distance_matrix(locations)
    route, min_distance = solve_tsp(distance_matrix)
    route_names = [locations[i]["name"] for i in route]
    return jsonify({"route": route_names, "distance": round(min_distance, 2)})

if __name__ == "__main__":
    app.run(debug=True)