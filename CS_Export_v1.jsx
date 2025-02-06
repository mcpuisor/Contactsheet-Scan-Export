// Photoshop JavaScript Script
var detectedImages = [
    {x: 219, y: 337, width: 1161, height: 2048},
    {x: 1942, y: 336, width: 1163, height: 2045},
    {x: 3660, y: 316, width: 1152, height: 2062},
    {x: 228, y: 2486, width: 1154, height: 2048},
    {x: 1942, y: 2485, width: 1156, height: 2046},
    {x: 3661, y: 2482, width: 1151, height: 2046},
    {x: 214, y: 4636, width: 1180, height: 2046},
    {x: 1944, y: 4634, width: 1153, height: 2046}
];

for (var i = 0; i < detectedImages.length; i++) {
    var img = detectedImages[i];
    
    // Select the rectangle area
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
    
    // Create a selection
    var doc = app.activeDocument;
    doc.selection.select(bounds);
    
    // Copy the selection to a new document
    doc.selection.copy();
    var newDoc = app.documents.add(width, height);
    newDoc.paste();
    
    // Export as JPEG
    var outputFile = new File("~/Desktop/test/image_" + i + ".jpg");
    exportJPEG(newDoc, outputFile);
    
    // Close the new document without saving
    newDoc.close(SaveOptions.DONOTSAVECHANGES);
}

function exportJPEG(doc, outputFile) {
    var jpegOptions = new JPEGSaveOptions();
    jpegOptions.quality = 12; // Highest quality
    doc.saveAs(outputFile, jpegOptions, true, Extension.LOWERCASE);
}