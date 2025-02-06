// Photoshop JavaScript Script
#include "R:/10_Projects/001_Delta/03_scan/4/test/coordinates.js"

// Process each scanned paper
for (var filename in detectedImagesByFile) {
    var coordinates = detectedImagesByFile[filename];
    
    // Open the scanned image file
    var file = new File(input_dir + "/" + filename);
    open(file);
    
    // Process each detected image
    for (var i = 0; i < coordinates.length; i++) {
        var img = coordinates[i];
        var x = img.x;
        var y = img.y;
        var width = img.width;
        var height = img.height;
        
        // Create selection bounds
        var bounds = [
            [x, y],
            [x + width, y],
            [x + width, y + height],
            [x, y + height]
        ];
        
        // Select and export
        var doc = app.activeDocument;
        doc.selection.select(bounds);
        doc.selection.copy();
        
        var newDoc = app.documents.add(width, height);
        newDoc.paste();
        
        var outputFile = new File("~/Desktop/test/" + filename.replace(/\.[^\.]+$/, "") + "_" + i + ".jpg");
        exportJPEG(newDoc, outputFile);
        
        newDoc.close(SaveOptions.DONOTSAVECHANGES);
    }
    
    // Close the scanned document
    app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
}

function exportJPEG(doc, outputFile) {
    var jpegOptions = new JPEGSaveOptions();
    jpegOptions.quality = 12;
    doc.saveAs(outputFile, jpegOptions, true, Extension.LOWERCASE);
}