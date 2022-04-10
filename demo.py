"""
demo.py
Spring 2022 PJW

Demonstrate projecting data, dissolving layers, and constructing 
buffers using geopandas.
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import fiona
import os

#%%
#  
#  Set up projection number and file names
#

utm18n = 26918
demo_file = 'demo.gpkg'
out_file = 'demo-output.gpkg'

#
#  List the layers in the input file and then read them
#

layers = fiona.listlayers(demo_file)
print( f'Layers in {demo_file}:', layers )

county = gpd.read_file(demo_file,layer='county')
zips   = gpd.read_file(demo_file,layer='zips')
water  = gpd.read_file(demo_file,layer='water')

#%%
#
#  Now project the layers to UTM 18N
#

county = county.to_crs(epsg=utm18n)
zips   = zips.to_crs(epsg=utm18n) 
water  = water.to_crs(epsg=utm18n) 

#%%
#
#  The water layer countains a lot of small streams: filter it down to
#  just things with names.
#

print('\nOriginal water records:', len(water) )

water = water.dropna(subset='FULLNAME')

print('\nWater records with names:', len(water) )

#%%
#
#  Many water bodies are split across multiple records.
#

print( water['FULLNAME'].value_counts().head() )

#
#  Combine geographies for water bodies with identical names
#

water_by_name = water.dissolve('FULLNAME')
water_by_name = water_by_name.reset_index()

print( water_by_name['FULLNAME'].value_counts().head() )

#%%
#  
#  Now find locations within about a mile of water. First, dissolve the water 
#  layer further so the geometries are combined into a single record. Then 
#  build a 1600 m buffer around it
#

water_dis = water_by_name.dissolve()

near_water = water_dis.buffer(1600)

#%%
#
#  Clip the zip codes and buffer at the county boundary. The 
#  keep_geom_type causes geopandas to close clipped polygons.
#

zips_clip = zips.clip(county,keep_geom_type=True)
near_clip = near_water.clip(county,keep_geom_type=True)

#%%
#
#  Check whether the output file exists and remove it if it does. 
#  Then write the layers.
#

if os.path.exists(out_file):
    os.remove(out_file)

zips.to_file(out_file,layer='zips_all',index=False)
zips_clip.to_file(out_file,layer='zips_clipped',index=False)
water_by_name.to_file(out_file,layer='water_bodies',index=False)
near_clip.to_file(out_file,layer='near_water',index=False)

#%%
#
#  Now draw a map with 4 layers: the county, the zip codes, the water layer,
#  and finally the near_water buffer.
#

fig1,ax1 = plt.subplots(dpi=300)
county.plot(color='tan',ax=ax1)
zips_clip.boundary.plot(color='black',linewidth=0.5,ax=ax1)
water.plot(color='xkcd:lightblue',ax=ax1)
near_clip.plot(alpha=0.25,ax=ax1)
ax1.axis('off')
