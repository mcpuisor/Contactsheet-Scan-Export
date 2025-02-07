#target photoshop
app.bringToFront();

// Prompt the user for a destination folder
var destFolder = Folder.selectDialog("Select a folder to save JPEG files");
if (destFolder == null) {
    // User cancelled the dialog
    throw new Error("No folder selected. Script cancelled.");
}

// Loop through all open documents
// Note: We use a for-loop on a snapshot of app.documents to avoid issues if documents change
var docs = app.documents;
for (var i = 0; i < docs.length; i++) {
    // Get a reference to the document
    var doc = docs[i];
    // Duplicate the document (so we don't affect the original)
    var dup = doc.duplicate();
    // Flatten the duplicate so it can be saved as JPEG (JPEG does not support layers)
    dup.flatten();
    
    // Remove any extension from the document name
    var baseName = dup.name.replace(/\.[^\.]+$/, "");
    // Create a File object for the output file in the selected folder
    var saveFile = new File(destFolder + "/" + baseName + ".jpg");
    
    // Set JPEG options with quality 12 (highest)
    var jpegOptions = new JPEGSaveOptions();
    jpegOptions.quality = 12; // Maximum quality
    
    // Save the duplicate as JPEG. The "true" argument tells Photoshop to use the current document’s color mode.
    dup.saveAs(saveFile, jpegOptions, true);
    // Close the duplicate without saving changes
    dup.close(SaveOptions.DONOTSAVECHANGES);
}

alert("Export complete!");
