import sys

import geopandas as gpd
import utm
from PIL import Image
from shapely.geometry import Point, Polygon
import rasterio
import numpy as np
import cv2
import os
import configuration
from configuration import *
import time
import random
import datetime


def createDirectoriesIfNotExist(directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
def find_bottom_right_top_left(points):
    if not points:
        return None, None

    bottom_right = [float('-inf'), float('-inf')]
    top_left = [float('inf'), float('inf')]

    for lat, lon in points:
        bottom_right[0] = max(bottom_right[0], lat)
        bottom_right[1] = max(bottom_right[1], lon)

        top_left[0] = min(top_left[0], lat)
        top_left[1] = min(top_left[1], lon)

    return tuple(top_left), tuple(bottom_right)


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
    temp_crop_type=None
    for i in range(startX, startX+xSize):
        for j in range(startY, startY+ySize):
            rasterMap[i-startX][j-startY][0]=raster.read(1)[i][j]
            rasterMap[i-startX][j-startY][1]=raster.read(2)[i][j]
            rasterMap[i-startX][j-startY][2]=raster.read(3)[i][j]

            val = raster.xy(i, j)
            lat, lon = utm.to_latlon(val[0], val[1], 35, northern=True)
            point = Point(lat, lon)

            if temp_poly:
                result = isPointInsidePolygon(point, temp_poly)
                if result:
                    color = CROP_COLOR_CODES[temp_crop_type]
                    rasterMask[i-startX][j-startY][0] = color[0]
                    rasterMask[i-startX][j-startY][1] = color[1]
                    rasterMask[i-startX][j-startY][2] = color[2]
                    continue
                else:
                    temp_poly=None
                    temp_crop_type=None



            for k, v in polygon_dict.items():
                flag = True
                for each_poly in v:
                    min_point_of_poly, max_point_of_poly = polygon_minmax_points_dict_train[tuple(each_poly)]
                    if min_point_of_poly[0] < lat < max_point_of_poly[0] and min_point_of_poly[1] < lon < max_point_of_poly[1]:
                        poly = Polygon(each_poly)
                        result = isPointInsidePolygon(point, poly)
                    else:
                        result=False
                    if result:
                        temp_poly = poly
                        temp_crop_type = k
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
    image.save("dataset_patches/imageRGB-" + str(xSize) + "-" + str(ySize) + "-" + str(startX) + "-" + str(startY) + ".png")

    rasterMask = np.clip(rasterMask, 0, 255).astype('uint8')
    image = Image.fromarray(rasterMask, 'RGB')
    image.save("dataset_masks/maskRGB-" + str(xSize) + "-" + str(ySize) + "-" + str(startX) + "-" + str(startY) + ".png")









createDirectoriesIfNotExist(["./dataset_patches", "./dataset_masks"])


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




polygon_minmax_points_dict_train = {}
for k, v in polygon_dict_train.items():
    for each_poly in v:
        polygon_minmax_points_dict_train[tuple(each_poly)] = find_bottom_right_top_left(each_poly)


#sys.exit(1)


rasterRGB = rasterio.open(COMPOSITE_RGB_TIF_FILE_PATH)

xSize = 64 #101
ySize = 64 #101
startX = [random.randint(0,1650), random.randint(0,1650), random.randint(0,1650), random.randint(0,1650)] #300
startY = [random.randint(0,2850), random.randint(0,2850), random.randint(0,2850), random.randint(0,2850), random.randint(0,2850)] #1500

number_of_patches = len(startX)*len(startY)

print(number_of_patches, "patches will be generated in total with size", str(xSize) + "x" + str(ySize))
print("Generation has started...")

start_time = time.time()

ct=1
for i in startX:
    for j in startY:
        start_time_temp = time.time()
        cutPatchAndCreateMask(rasterRGB, xSize, ySize, i, j, polygon_dict_train)
        end_time_temp = time.time()
        print("Successfully generated patch", "#"+str(ct)+"#")
        #print("Time Taken:", datetime.timedelta(seconds=end_time_temp - start_time_temp))
        minutes = int(divmod((number_of_patches - ct)*(end_time_temp - start_time_temp), 60)[0])
        seconds = int(divmod((number_of_patches - ct)*(end_time_temp - start_time_temp), 60)[1])
        print('{} minutes {} seconds left'.format(minutes, seconds))
        ct+=1

end_time = time.time()
print("Done...")
print("Total time taken:", '{} minutes {} seconds'.format(*divmod(end_time - start_time, 60)))
