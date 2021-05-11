# Exercise: Building a Buffer Around a Highway

### Summary

This exercise uses geopandas to project Census shapefiles appropriately for New York State. It then builds several map layers for Onondaga County, including a 1-km buffer around the county's interstate highways.

### Input Data

There are two input files, both of which are TIGER/Line shapefiles that will be downloaded from the Census in part A of the instructions.

### Deliverables

There are three deliverables: a script called **onondaga.py**, a QGIS project file called **highway.qgz**, and an image file called **highway.png**.

### Instructions

**A. Downloading files from the Census**

1. Go to the Census TIGER/Line page (there's a link on the class web site) and then click on the link for the web interface. Select 2020 and then download two files: "Counties (and equivalent)", which should be `tl_2020_us_county.zip`, and "Roads > Primary and Secondary Roads > New York", which should be `tl_2020_36_prisecroads.zip`.

**B. Script onondaga.py**

1. Import `geopandas`.

1. Use the `geopandas.read_file()` function to read the Census county shapefile into a variable called `county`. 

1. Create a variable called `on_county` by using the `.query()` method of `county` to select Onondaga County using its state and county FIPS codes. The columns for the FIPS codes are `"STATEFP"` and `"COUNTYFP"`. The state and county codes for Onondaga are probably familiar by now but just to avoid confusion they are `"36"` and `"067"`.

1. Create a variable called `on_border` that is equal to the `"geometry"` field of `on_county`. It will be the polygon describing the county's border and will be used below to clip the road layer.

1. Use the `geopandas.read_file()` function to read the primary and secondary roads file into a variable called `roads`. 

1. Create a variable called `interstates` by using the `.query()` method of `roads` to select the records where the route type, `"RTTYP"`, is equal to `"I"`, the code for interstates. 

1. Now clip the interstate layer at the county boundary by setting `on_interstates` to the result of calling the `geopandas.clip()` function with three arguments: `interstates`, which is the layer to be clipped, `on_border`, the polygon created above that indicates the border for clipping, and `keep_geom_type=True`, which indicates that the clipped file should have only features of the type originally in the layer being clipped (lines, in this case). Without the `keep_geom_type=True` argument, the clipped layer will also include a separate set of points at the places where the roads cross the county boundary. 

1. Now build a projected version of the county border using the projection recommended for the state by the New York State GIS Clearinghouse: NAD83(2011)/UTM Zone 18N, which is also known as EPSG:6347. Set `pro_county` to the result of calling the `.to_crs()` method of `on_county` using argument `epsg=6347`. For future reference, the units of the projected coordinate system will be meters.

1. Create a projected version of the interstate layer called `pro_interstates` by applying `.to_crs()` to `on_interstates`.

1. Now dissolve the polygons in the projected interstate layer to create a single feature representing all of the interstates in the county. The dissolved layer should be called `dis_interstates` and it should be created by calling the `.dissolve()` method of `pro_interstates` with the arguments `by="RTTYP"` and `aggfunc="first"`. See the Tips section for more information about what dissolving a layer does.
    
1. Now create a layer called `buffer` that is equal to the result of calling the `.buffer()` method of `dis_interstates` with argument `1000`. Because the units of the coordinate system are meters, the 1000 indicates that the buffer should be 1000 meters, or 1 km, wide.

1. Save `pro_county` to a geopackage file by using its `.to_file()` method with `"onondaga.gpkg"` as the file name, `"county"` as the layer name, and `"GPKG"` as the driver.

1. Save `pro_interstates` to the same geopackage file but with layer name `"interstates"`.

1. Save `buffer` to the same geopackage file but with layer name `"buffer"`.

**C. Files highway.qgz and highway.png**

1. Start QGIS and load the geopackage file created by the previous script.

1. Stack the layers so that the interstate layer is on top, then the buffer, and then the county. 

1. Set the colors as you see fit and then save the project file as `"highway.qgz"`. 

1. Finally, export the map to a PNG file called `highway.png`.

### Submitting

Once you're happy with everything and have committed all of the changes to your local repository, please push the changes to GitHub. At that point, you're done: you have submitted your answer.

### Tips

+ Dissolving a layer is a form of aggregation and is the geographic equivalent of combining the Pandas `groupby()` and `agg()` functions. The `by=` argument indicates how the groups should be formed: here it says that all features with the same value of `"RTTYP"` should be grouped together (all the interstate segments, in this case). The `aggfunc=` argument indicates how the attributes for the grouped data are to be set. Here, `"first"` says that the attributes should be set to their values for the first object in each group. There are a number of options, including `"first"`, `"last"`, `"sum"`, `"max"`, `"mean"`, and `"median"`. However, we're not going to use the attributes so we'll use `"first"` for simplicity since it works for both string and numeric fields. It's also the default if no option is specified.

+ This is the start of a multi-part exercise that will involve classifying residential properties in the county by their proximity to the interstates.
