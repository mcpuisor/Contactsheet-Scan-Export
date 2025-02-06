# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

def get_input_directory():
    """Prompt the user to enter the directory path."""
    while True:
        path = input("Enter the directory path containing scanned images: ").strip()
        # Remove quotes if user accidentally includes them
        path = path.strip('"').strip("'")
        if os.path.exists(path):
            return path
        else:
            print(f"Error: The directory '{path}' does not exist. Please try again.")

def detect_images(image_path):
    """Detect and sort images in left-to-right, top-to-bottom order."""
    image = cv2.imread(image_path)
    if image is None:
        return None

    # Preprocess image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract coordinates and filter by area
    detected = []
    for contour in contours:
        if cv2.contourArea(contour) > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            detected.append((x, y, w, h))

    # Group into rows using y-coordinate tolerance
    detected.sort(key=lambda rect: rect[1])  # Preliminary sort by y
    rows = []
    current_row = []
    prev_y = None

    for rect in detected:
        x, y, w, h = rect
        if prev_y is None or abs(y - prev_y) <= y_tolerance:
            current_row.append(rect)
        else:
            rows.append(current_row)
            current_row = [rect]
        prev_y = y

    if current_row:
        rows.append(current_row)

    # Sort each row left-to-right (by x), then all rows top-to-bottom (by y)
    sorted_coords = []
    for row in rows:
        row_sorted = sorted(row, key=lambda rect: rect[0])  # Left-to-right
        sorted_coords.extend(row_sorted)

    return sorted_coords

def main():
    # Get user input for directory
    input_dir = get_input_directory()
    output_js_path = os.path.join(input_dir, 'coordinates.js')
    min_area = 1000  # Minimum contour area to detect
    y_tolerance = 20  # Vertical tolerance for grouping rows

    # Create output directory if it doesn’t exist
    os.makedirs(os.path.dirname(output_js_path), exist_ok=True)

    # Get all image files in the input directory
    image_files = [
        f for f in os.listdir(input_dir)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    # Process each image and store coordinates
    all_coordinates = {}
    for filename in image_files:
        filepath = os.path.join(input_dir, filename)
        coordinates = detect_images(filepath)
        if coordinates:
            all_coordinates[filename] = coordinates

    # Generate JavaScript output
    js_output = f"var input_dir = '{input_dir.replace('\\', '/')}';\n"
    js_output += "var detectedImagesByFile = {\n"
    
    for i, (filename, coords) in enumerate(all_coordinates.items()):
        js_output += f'  "{filename}": [\n'
        for j, (x, y, w, h) in enumerate(coords):
            js_output += f'    {{x: {x}, y: {y}, width: {w}, height: {h}}}'
            js_output += ',\n' if j < len(coords)-1 else '\n'
        js_output += '  ]' + (',\n' if i < len(all_coordinates)-1 else '\n')
    js_output += "};\n"

    # Save to JS file
    with open(output_js_path, 'w') as f:
        f.write(js_output)
    print(f"Saved coordinates to {os.path.abspath(output_js_path)}")

if __name__ == '__main__':
    main()