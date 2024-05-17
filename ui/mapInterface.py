import folium
import numpy as np
import random

distance = 0.01

latA = 38.54714
lonA = 28.00335
latB = 38.54714 + distance
lonB = 28.00335 + distance
precision = 4


mapObj = folium.Map(location=[38.56, 28.01],
                    zoom_start=13)

np.arange(latA, latB + (latB-latA)/precision, (latB-latA)/precision)

for i in np.arange(latA, latB + (latB-latA)/precision, (latB-latA)/precision):
    for j in np.arange(lonA, lonB + (lonB-lonA)/precision, (lonB-lonA)/precision):
        lat1 = i
        lon1 = j
        lat2 = i + (latB-latA)/precision
        lon2 = j + (lonB-lonA)/precision

        color = "%06x" % random.randint(0, 0xFFFFFF)

        folium.Polygon([
        (lat2, lon1),
        (lat2, lon2),
        (lat1, lon2),
        (lat1, lon1)
        ],
                   stroke=False,
                   color="#a632a8",
                   weight=2,
                   fill=True,
                   fill_color="#"+color,
                   fill_opacity=0.4).add_to(mapObj)

mapObj.save('output.html')
