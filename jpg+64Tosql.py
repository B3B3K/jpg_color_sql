import cv2
import numpy as np
import base64
import sqlite3

# Load the image
image_path = "test_r.jpg"
image = cv2.imread(image_path)
h, w, _ = image.shape

# Print the height and width
print(f"Height (h): {h} pixels")
print(f"Width (w): {w} pixels")

# Define the size of each split area
split_size = 2

# Get the dimensions of the image
height, width, _ = image.shape

# Create an empty list to store the average color and coordinates of each split area
split_areas = []

# Iterate over the image in split_size intervals
for y in range(0, height, split_size):
    for x in range(0, width, split_size):
        # Calculate the coordinates of the split area
        x1 = x
        y1 = y
        x2 = x + split_size
        y2 = y + split_size

        # Extract the split area from the image
        split_area = image[y1:y2, x1:x2]

        # Calculate the average color of the split area
        average_color = np.mean(split_area, axis=(0, 1))

        # Store the average color and coordinates in the list
        split_areas.append((x1, y1, x2, y2, average_color))

# Create a SQLite database connection
db_conn = sqlite3.connect("split_areas.db")
cursor = db_conn.cursor()

# Create the table for split areas data
cursor.execute("CREATE TABLE IF NOT EXISTS split_areas ("
               "id INTEGER PRIMARY KEY AUTOINCREMENT,"
               "x1 INTEGER,"
               "y1 INTEGER,"
               "x2 INTEGER,"
               "y2 INTEGER,"
               "average_color TEXT)")

# Insert the split areas data into the table
for x1, y1, x2, y2, color in split_areas:
    # Convert the average color values from float to integer
    color_int = color.astype(int)
    # Convert the color values to a string for storage in the database
    color_str = ','.join(map(str, color_int))
    
    # Insert the data into the table
    cursor.execute("INSERT INTO split_areas (x1, y1, x2, y2, average_color) "
                   "VALUES (?, ?, ?, ?, ?)",
                   (x1, y1, x2, y2, color_str))

# Commit the changes and close the database connection
db_conn.commit()
db_conn.close()
