import cv2
import numpy as np

# Load the scanned paper image
image = cv2.imread(r'R:\10_Projects\001_Delta\03_scan\4\img2.jpg')
if image is None:
    print("Error: Image not found.")
    exit()

# Convert to grayscale and threshold
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours based on area (adjust min_area as needed)
min_area = 1000
detected_images = []
for contour in contours:
    if cv2.contourArea(contour) > min_area:
        x, y, w, h = cv2.boundingRect(contour)
        detected_images.append((x, y, w, h))

# Sort detected images into rows (top-to-bottom), then left-to-right within each row
# ----------------------------------------------------------------------------------
# 1. Sort all images by y (top-to-bottom) to group rows
detected_images.sort(key=lambda rect: rect[1])

# 2. Group images into rows using a y-coordinate tolerance (adjust as needed)
y_tolerance = 20  # Max vertical difference to consider images part of the same row
rows = []
current_row = []
prev_y = None

for img in detected_images:
    x, y, w, h = img
    if prev_y is None or abs(y - prev_y) <= y_tolerance:
        current_row.append(img)
    else:
        rows.append(current_row)
        current_row = [img]
    prev_y = y

if current_row:
    rows.append(current_row)

# 3. Sort each row by x-coordinate in ascending order (left-to-right)
sorted_images = []
for row in rows:
    # Sort the row by x in ascending order (smallest x first)
    row_sorted = sorted(row, key=lambda rect: rect[0])
    sorted_images.extend(row_sorted)

# Print coordinates in JavaScript-compatible format
js_output = "var detectedImages = [\n"
for i, (x, y, w, h) in enumerate(sorted_images):
    js_output += f"    {{x: {x}, y: {y}, width: {w}, height: {h}}}"
    if i < len(sorted_images) - 1:
        js_output += ",\n"
    else:
        js_output += "\n"
js_output += "];"

print(js_output)