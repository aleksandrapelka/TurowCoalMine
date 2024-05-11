import ee
import geemap.foliumap as geemap
from maps.visualization import get_vis_params, get_breaks, get_labels, get_palette
import data.data as data


projection = {'crs': 'EPSG:32633', 'transform': [10, 0, 399960, 0, -10, 5600040]}

def get_image(index_name, date, collection):
   collection = collection.select(index_name)
   image = ee.Image(collection.filterMetadata('date', 'equals', date).first())
   image = image.reproject(crs=projection['crs'], crsTransform=projection['transform'])

   return image

def classify_image(index_name, image):
   breaks = get_breaks()[index_name]
   image = image.updateMask(image.gte(breaks[0]).And(image.lte(breaks[10])))
   image = image.gte(breaks[0]).add(image.gte(breaks[1])).add(image.gte(breaks[2])).add(image.gte(breaks[3])).add(image.gte(breaks[4])).add(image.gte(breaks[5])).add(image.gte(breaks[6])).add(image.gte(breaks[7])).add(image.gte(breaks[8])).add(image.gte(breaks[9]).And(image.lte(breaks[10])))

   return image

def get_classified_image(index_name, date, collection):
   image = get_image(index_name, date, collection)
   classified_image = classify_image(index_name, image)

   return classified_image

# def detect_chages(image1, image2):
#    threshold = 0.2
#    change = image2.subtract(image1)
#    change = change.updateMask(change.abs().gt(threshold))
#    classified_changes = change.gt(-100).add(change.gt(0))

#    return classified_changes

def detect_chages(image1, image2):
   threshold = 0.3
   change = image2.subtract(image1)
   change = change.updateMask(change.abs().gt(threshold))
   classified_changes = change.gt(-100).add(change.gt(-0.6)).add(change.gt(0)).add(change.gt(0.6))

   return classified_changes
   
def add_image_to_map(image, index_name, label):
   vis_params = get_vis_params()
   map = geemap.Map(basemap="Esri.WorldGrayCanvas") #"CartoDB.DarkMatterNoLabels","CartoDB.DarkMatter","BasemapAT.grau", "Esri.WorldGrayCanvas","Esri.WorldShadedRelief"
   map.centerObject(data.selected_units, 11)
   map.addLayer(image, vis_params[index_name], label)
   map.add_legend(title=index_name, colors=get_palette()[index_name], labels=get_labels()[index_name])
   #map.add_colorbar(vis_params[index_name], categorical=True, index=get_breaks()[index_name][:-1])
   map.to_streamlit()
