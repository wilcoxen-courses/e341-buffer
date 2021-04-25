# Exercise: Selecting Parcels Near an Interstate

### Summary

This exercise uses QGIS to identify tax parcels that are near one of 
the Interstate highways in Onondaga County.

### Input Data

There are three input files. The first two are TIGER/Line shapefiles that 
will be downloaded from the Census below. The third is a file of tax 
parcel centroids called `Onondaga-Tax-Parcels-Centroid-Points-SHP.zip`
that can be downloaded from the class Google Drive directory for this
exercise.

### Deliverables

There are three deliverables: a QGIS project file called **highway.qgz**, 
a GeoPackage file called **onondaga.gpkg**, and a PNG file called 
**highway.png**.

### Instructions

1. Go to the Census TIGER/Line page and then to the web interface. Select 
2018 and then download two layers: (1) "Counties (and equivalent)", which 
should be `tl_2018_us_county.zip`, and (2) "Roads" -> "Primary and 
Secondary Roads" -> "New York", which should be `tl_2018_36_prisecroads.zip`.

1. Load the counties layer into QGIS and filter it down to Onondaga 
County using `"STATEFP"` equal to `'36'` and `"COUNTYFP"` equal to `'067'`.
Note that single and double quotes are **not** equivalent in QGIS: double 
quotes are used with variable names and single quotes are used with 
strings. If you build the query by clicking on the variable name under 
"Fields" and the value under "Values" QGIS will use the correct 
quoting.

1. Change the project projection using the button with the globe icon
at the lower right. Set it to EPSG:6347 "NAD83(2011) / UTM Zone 18N", which 
is the New York State GIS Clearinghouse recommended projection. The county 
should become narrower and look like it usually does in other maps.

1. Export the resulting layer to a GeoPackage file called `onondaga.gpkg`
in the GitHub directory for the assignment. Call the layer itself 
`boundary` and make sure the "Add saved file to map" box is checked. Then 
remove the original layer to leave a single layer called 
`onondaga boundary`.

1. Add the roads layer to the map. Then filter it down to interstates only 
using `"RTTYP"` equal to `'I'`.

1. Now clip the roads using the county boundary. Export the layer to 
the GeoPackage file you created above but use the layer name `interstates`
and set the coordinate reference system (CRS) to the project CRS, which 
should now be EPSG:6347. 

1. Remove both the original road layer and the layer called `Clipped`.
You should end up with two layers: one called `onondaga boundary` and 
one called `onondaga interstates`.

1. Select `onondaga interstates` and create a buffer using a distance of 
500 meters. Scroll down and check the "Dissolve result" box. Save the 
buffer in the GeoPackage file with the layer name `buffer 500m`. Then 
remove the `Buffered` layer.

1. Add the tax parcel centroid layer.

1. Clip the parcel layer using `buffer 500m` as the overlay. 

1. Uncheck the original parcel layer. That should leave the parcels that 
are within 500 meters of the highways.

1. Save the project in the GitHub directory as `highway.qgz`.

1. Export the map to a PNG file called `highway.png`.

### Submitting

Once you're happy with everything and have committed all of the changes to
your local repository, please push the changes to GitHub. At that point, 
you're done: you have submitted your answer.

### Tips

+ In practice, a study like this would usually go further by exporting the 
clipped parcels to a CSV file so they could be subjected to further 
statistical analysis. We'll do that in a subsequent exercise involving 
additional buffers.