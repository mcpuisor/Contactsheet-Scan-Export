This is a script that will help out when working with Contact Sheets in Photoshop.


**Export_All_Docs.jsx** - This will export all opened files from Photoshop to a desired location, provided by user.

**Mask_Batch.py** - This is reading out the images coordinates from each file, generating a **Coordinates.js** that keeps all information and a **JS script** that has to be run in Photoshop later for exporting the images as per the coordinates documented.

Exports will be always stored in a new folder called **Export** in the same folder as the images, coordinates and JS script.

The script can be executed via the **Execute batch** bat file.

**Printing coordinates single file** does the same as first script above, but for only one image. Image path has to be provided.

**Mask Export single file** does the same as the above JS script, but for only the opened file in Photoshop.
