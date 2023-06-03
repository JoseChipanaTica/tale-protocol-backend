import random

# Define the box's corners (latitude, longitude)
corner1 = (-1.1762060103540677, 20.58353045741974)
corner2 = (-0.9015932197136295, 21.33060076991974)
corner3 = (-2.5514825140007673, 21.98154071132599)
corner4 = (-1.9202527792750042, 22.75058368007599)

# Calculate the latitude and longitude range
min_lat = min(corner1[0], corner2[0], corner3[0], corner4[0])
max_lat = max(corner1[0], corner2[0], corner3[0], corner4[0])
min_lng = min(corner1[1], corner2[1], corner3[1], corner4[1])
max_lng = max(corner1[1], corner2[1], corner3[1], corner4[1])

# Generate random unique points within the box
num_points = 1000
points = set()

while len(points) < num_points:
    lat = random.uniform(min_lat, max_lat)
    lng = random.uniform(min_lng, max_lng)
    points.add((lat, lng))

# Display the generated points
for point in points:
    print(
        f"('zebra', 'https://img.icons8.com/flat-round/64/funny-zebra.png', st_point({point[1]}, {point[0]}))")
