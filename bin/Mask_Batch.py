# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

def get_input_directory():
    """Prompt the user to enter the directory path."""
    while True:
        path = input("Enter the directory path containing scanned images: ").strip()
        path = path.strip('"').strip("'")
        if os.path.exists(path):
            return path
        else:
            print(f"Error: The directory '{path}' does not exist. Please try again.")

def detect_images(image_path, min_area, y_tolerance):
    """Detect and sort images in left-to-right, top-to-bottom order."""
    image = cv2.imread(image_path)
    if image is None:
        return None

    # Preprocess image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract coordinates and filter by area/size
    detected = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Skip regions smaller than 50x50 pixels and min_area
        if cv2.contourArea(contour) > min_area and w >= 50 and h >= 50:
            detected.append((x, y, w, h))

    # Group into rows using y-coordinate tolerance
    detected.sort(key=lambda rect: rect[1])
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

    # Sort each row left-to-right
    sorted_coords = []
    for row in rows:
        row_sorted = sorted(row, key=lambda rect: rect[0])
        sorted_coords.extend(row_sorted)

    return sorted_coords

def main():
    input_dir = get_input_directory()
    output_js_path = os.path.join(input_dir, 'coordinates.js')
    output_jsx_path = os.path.join(input_dir, 'Execute in PS.jsx')
    min_area = 1000
    y_tolerance = 20

    os.makedirs(os.path.dirname(output_js_path), exist_ok=True)

    # Get image files
    image_files = [
        f for f in os.listdir(input_dir)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    # Process images
    all_coordinates = {}
    for filename in image_files:
        filepath = os.path.join(input_dir, filename)
        coordinates = detect_images(filepath, min_area, y_tolerance)
        if coordinates:
            all_coordinates[filename] = coordinates

    # Generate coordinates.js
    js_output = f"var input_dir = '{input_dir.replace('\\', '/')}';\n"
    js_output += "var detectedImagesByFile = {\n"
    
    for i, (filename, coords) in enumerate(all_coordinates.items()):
        js_output += f'  "{filename}": [\n'
        for j, (x, y, w, h) in enumerate(coords):
            js_output += f'    {{x: {x}, y: {y}, width: {w}, height: {h}}}'
            js_output += ',\n' if j < len(coords)-1 else '\n'
        js_output += '  ]' + (',\n' if i < len(all_coordinates)-1 else '\n')
    js_output += "};\n"

    with open(output_js_path, 'w') as f:
        f.write(js_output)
    print(f"Saved coordinates to {os.path.abspath(output_js_path)}")

    # Generate JSX file with corrected path
    processed_js_path = output_js_path.replace('\\', '/')
    jsx_template = r'''// Photoshop JavaScript Script
#include "{processed_js_path}"

for (var filename in detectedImagesByFile) {{
    var coordinates = detectedImagesByFile[filename];
    var file = new File(input_dir + "/" + filename);
    open(file);
    
    for (var i = 0; i < coordinates.length; i++) {{
        var img = coordinates[i];
        var x = img.x;
        var y = img.y;
        var width = img.width;
        var height = img.height;
        
        var bounds = [
            [x, y],
            [x + width, y],
            [x + width, y + height],
            [x, y + height]
        ];
        
        var doc = app.activeDocument;
        doc.selection.select(bounds);
        doc.selection.copy();
        
        var newDoc = app.documents.add(width, height);
        newDoc.paste();
        
        var outputFile = new File(input_dir + "/exports/" + filename.replace(/\.[^.]+$/, "") + "_" + i + ".jpg");
        outputFile.parent.create();
        exportJPEG(newDoc, outputFile);
        
        newDoc.close(SaveOptions.DONOTSAVECHANGES);
    }}
    app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
}}

function exportJPEG(doc, outputFile) {{
    var jpegOptions = new JPEGSaveOptions();
    jpegOptions.quality = 12;
    doc.saveAs(outputFile, jpegOptions, true, Extension.LOWERCASE);
}}
'''.format(processed_js_path=processed_js_path)

    with open(output_jsx_path, 'w') as f:
        f.write(jsx_template)
    print(f"Saved JSX processor to {os.path.abspath(output_jsx_path)}")

if __name__ == '__main__':
    main()