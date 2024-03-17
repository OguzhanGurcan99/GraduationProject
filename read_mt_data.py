import geopandas as gpd
import utm
from PIL import Image
from shapely.geometry import Point, Polygon
import rasterio
import numpy as np
import cv2

import configuration
from configuration import *

def isPointInsidePolygon(point, polygon):
    '''
    # Point objects(Geo-coordinates)
    p1 = Point(24.952242, 60.1696017)
    p2 = Point(24.976567, 60.1612500)

    # Polygon
    coords = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
    poly = Polygon(coords)
    '''
    return polygon.contains(point) or polygon.touches(point)

def read_shp_file(path):
    shapefile = gpd.read_file(path)
    total_list=[]
    for i in range(len(shapefile["geometry"])):
        ls = list(shapefile["geometry"][i].exterior.coords)
        converted_list = []
        for j in ls:
            lat, lon = utm.to_latlon(j[0], j[1], 35, northern=True)
            converted_list.append((lat, lon))
        total_list.append(converted_list)
    return total_list

def cutPatchAndCreateMask(raster, xSize, ySize, startX, startY, polygon_dict):
    rasterMap = np.zeros((xSize, ySize, 3))
    rasterMask = np.zeros((xSize, ySize, 3))
    temp_poly=None
    for i in range(startX, startX+xSize):
        for j in range(startY, startY+ySize):
            rasterMap[i-startX][j-startY][0]=raster.read(1)[i][j]
            rasterMap[i-startX][j-startY][1]=raster.read(2)[i][j]
            rasterMap[i-startX][j-startY][2]=raster.read(3)[i][j]

            val = raster.xy(i, j)
            lat, lon = utm.to_latlon(val[0], val[1], 35, northern=True)
            point = Point(lat, lon)
            '''
            if temp_poly:
                result = isPointInsidePolygon(point, poly)
                if result:
                    rasterMask[i-startX][j-startY][0] = CROP_COLOR_CODES[k][0]
                    rasterMask[i-startX][j-startY][1] = CROP_COLOR_CODES[k][1]
                    rasterMask[i-startX][j-startY][2] = CROP_COLOR_CODES[k][2]
                else:
                    temp_poly=None
                continue
            '''

            for k, v in polygon_dict.items():
                flag = True
                for each_poly in v:
                    poly = Polygon(each_poly)
                    result = isPointInsidePolygon(point, poly)
                    if result:
                        temp_poly = poly
                        flag = False
                        color = CROP_COLOR_CODES[k]
                        rasterMask[i-startX][j-startY][0] = color[0]
                        rasterMask[i-startX][j-startY][1] = color[1]
                        rasterMask[i-startX][j-startY][2] = color[2]
                        break
                if flag:
                    rasterMask[i-startX][j-startY][0] = 0
                    rasterMask[i-startX][j-startY][1] = 0
                    rasterMask[i-startX][j-startY][2] = 0
                else:
                    break

    rasterMap = np.clip(rasterMap, 0, 255).astype('uint8')
    image = Image.fromarray(rasterMap, 'RGB')
    image.save("imageRGB" + str(xSize) + "-" + str(ySize) + "-" + str(startX) + "-" + str(startY) + ".png")

    rasterMask = np.clip(rasterMask, 0, 255).astype('uint8')
    image = Image.fromarray(rasterMask, 'RGB')
    image.save("maskRGB" + str(xSize) + "-" + str(ySize) + "-" + str(startX) + "-" + str(startY) + ".png")



bugday_polygons_train = read_shp_file(BUGDAY_SHP_FILE_PATH)
domates_polygons_train = read_shp_file(DOMATES_SHP_FILE_PATH)
misir_polygons_train = read_shp_file(MISIR_SHP_FILE_PATH)
misir2_polygons_train = read_shp_file(MISIR2_SHP_FILE_PATH)
pamuk_polygons_train = read_shp_file(PAMUK_SHP_FILE_PATH)
uzum_polygons_train = read_shp_file(UZUM_SHP_FILE_PATH)
yonca_polygons_train = read_shp_file(YONCA_SHP_FILE_PATH)
zeytin_polygons_train = read_shp_file(ZEYTIN_SHP_FILE_PATH)

polygon_dict_train = {"bugday" : bugday_polygons_train,
                "domates" : domates_polygons_train,
                "misir" : misir_polygons_train,
                "misir2" : misir2_polygons_train,
                "pamuk" : pamuk_polygons_train,
                "uzum" : uzum_polygons_train,
                "yonca" : yonca_polygons_train,
                "zeytin" : zeytin_polygons_train}


rasterRGB = rasterio.open(COMPOSITE_RGB_TIF_FILE_PATH)

xSize = 101
ySize = 101
startX = 300
startY = 1500
'''
ct=0
for i in range(300, 700, 200):
   for j in range(1500, 1900, 200):
        cutPatchAndCreateMask(rasterRGB, 101, 101, i, j, polygon_dict_train)
        print(ct)
        ct+=1
'''
cutPatchAndCreateMask(rasterRGB, xSize, ySize, startX, startY, polygon_dict_train)
