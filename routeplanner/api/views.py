import requests
from django.http import JsonResponse
from .models import FuelPrice
from django.db.models import Avg
from geopy.distance import geodesic

def get_route(request):
    # 1. Get the start and finish locations from the request
    start = request.GET.get('start')
    finish = request.GET.get('finish')

    if not start or not finish:
        return JsonResponse({"error": "Start and finish locations are required"}, status=400)

    # 2. Parse the coordinates
    try:
        start_coords = [float(coord) for coord in start.split(',')]
        finish_coords = [float(coord) for coord in finish.split(',')]
    except ValueError:
        return JsonResponse({"error": "Invalid coordinates format. Expected 'latitude,longitude'."}, status=400)

    try:
        # 3. Call the OpenRouteService API to get the route
        api_key = '5b3ce3597851110001cf624826d760185643492cbd541733f5d1d8e3'  # Replace with your OpenRouteService API key
        url = 'https://api.openrouteservice.org/v2/directions/driving-car'
        headers = {'Authorization': api_key}
        params = {
            'start': f"{start_coords[1]},{start_coords[0]}",
            'end': f"{finish_coords[1]},{finish_coords[0]}"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            route_data = response.json()
        else:
            return JsonResponse({"error": f"Failed to fetch route. Status Code: {response.status_code}"}, status=500)

        # 4. Calculate the route distance (in kilometers)
        distance = 0
        if 'features' in route_data and route_data['features']:
            distance = route_data['features'][0]['properties']['segments'][0]['distance'] / 1000  # Convert to kilometers

        # 5. Calculate fuel needs and cost
        fuel_efficiency = 10  # Vehicle's efficiency: 10 miles per gallon
        max_range = 500  # Maximum range of 500 miles
        fuel_needed = distance / (fuel_efficiency * 1.60934)  # Convert distance to gallons
        total_cost = 0

        # 6. Calculate average fuel cost
        fuel_prices = FuelPrice.objects.all()
        if fuel_prices.exists():
            average_price = fuel_prices.aggregate(Avg('retail_price'))['retail_price__avg']
            total_cost = fuel_needed * average_price  # Total fuel cost

        # 7. Calculate fuel stops along the route
        fuel_stops = []

        route_distance = geodesic(start_coords, finish_coords).miles

        if route_distance > max_range:
            fuel_stations = FuelPrice.objects.all()  # Fetch all fuel stations from the database
            for station in fuel_stations:
                station_coords = (station.latitude, station.longitude)
                distance_to_station = geodesic(start_coords, station_coords).miles

                if distance_to_station <= max_range:
                    fuel_stops.append({
                        "station_name": station.truckstop_name,
                        "station_location": f"{station.latitude},{station.longitude}",
                        "price": station.retail_price,
                        "distance_to_station_miles": round(distance_to_station, 2)
                    })

        # 8. Return the results as a JSON response
        result = {
            "start": start,
            "finish": finish,
            "distance_km": round(distance, 2),
            "fuel_needed_gallons": round(fuel_needed, 2),
            "total_cost_usd": round(total_cost, 2),
            "route": route_data['features'][0]['geometry'] if 'features' in route_data else None,
            "fuel_stops": fuel_stops
        }

        return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
