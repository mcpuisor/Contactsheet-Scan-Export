import cv2
import numpy as np
import os

# Configuration
input_dir = r'R:\10_Projects\001_Delta\03_scan\4\test'  # Directory containing scanned images
output_js_path = os.path.join(input_dir, 'coordinates.js')  # Output JS file path
min_area = 1000  # Minimum contour area to detect
y_tolerance = 20  # Vertical tolerance for grouping rows

def detect_images(image_path):
    """Detect and sort images in a single scanned paper (LEFT-TO-RIGHT)."""
    image = cv2.imread(image_path)
    if image is None:
        return None

    # Preprocess image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter and extract coordinates
    detected = []
    for contour in contours:
        if cv2.contourArea(contour) > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            detected.append((x, y, w, h))

    # Sort left-to-right, top-to-bottom (KEY FIX)
    detected.sort(key=lambda rect: (rect[1], rect[0]))  # Sort by y (top-to-bottom), then x (left-to-right)
    return detected

def main():
    # Create output directory if it doesn't exist
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