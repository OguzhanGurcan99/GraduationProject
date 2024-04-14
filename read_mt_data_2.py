import geopandas as gpd
import utm
from PIL import Image
from shapely.geometry import Point, Polygon
import rasterio
import numpy as np
import os
import configuration
from configuration import *


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

def cutPatchAndCreateMask(raster, xSize, ySize, startX, startY, polygons, min_max_points):
    rasterMap = np.zeros((xSize, ySize, 1))
    rasterMask = np.zeros((xSize, ySize, 1))
    temp_poly=None
    for i in range(startX, startX+xSize):
        for j in range(startY, startY+ySize):
            rasterMap[i-startX][j-startY]=raster.read(1)[i][j]
            val = raster.xy(i, j)
            lon, lat = val
            point = Point(lat, lon)
            if temp_poly:
                result = isPointInsidePolygon(point, temp_poly)
                if result:
                    rasterMask[i-startX][j-startY] = 255
                    continue
                else:
                    temp_poly=None

            flag = True
            for each_poly in polygons:
                min_point_of_poly, max_point_of_poly = min_max_points[tuple(each_poly)]
                if min_point_of_poly[0] < lat < max_point_of_poly[0] and min_point_of_poly[1] < lon < max_point_of_poly[1]:
                    poly = Polygon(each_poly)
                    result = isPointInsidePolygon(point, poly)
                else:
                    result=False
                if result:
                    temp_poly = poly
                    flag = False
                    rasterMask[i-startX][j-startY] = 255
                    break
            if flag:
                rasterMask[i-startX][j-startY] = 0
            else:
                pass

    return (rasterMap, rasterMask)

def createImageAndPatches(patch_dir, mask_dir, shapefile_path, xSize, ySize, x, y):
    createDirectoriesIfNotExist([patch_dir, mask_dir])
    polygons = read_shp_file(shapefile_path)
    min_max_points = create_polygon_minmax_points_dict(polygons)

    rasters = [
        rasterio.open(configuration._04_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._04_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._04_VV_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._07_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._07_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._07_VV_VH_TIFF_FILE_PATH)
    ]

    #row, col = raster1.index(x[0], y[0])
    #val = raster1.xy(450, 1610)
    #crs_x, crs_y = raster1.xy(880, 2140)
    #pixel_value = raster1.read(1)[row, col]

    for i in x:
        for j in y:
            rasterMaps = []
            rasterMasks = []
            for raster in rasters:
                row, col = raster.index(i, j)
                rasterMap, rasterMask = cutPatchAndCreateMask(raster, xSize, ySize, row, col, polygons, min_max_points)
                rasterMaps.append(rasterMap)
                rasterMasks.append(rasterMask)
            rasterMaps = np.array(rasterMaps)
            stackedMaps = np.squeeze(rasterMaps, axis=-1)
            np.save(patch_dir+"/" + str(xSize) + "-" + str(ySize) + "-" + str(i).replace(".", "dot") + "_" + str(j).replace(".", "dot") + ".npy", stackedMaps)
            count=1
            for m in rasterMasks:
                tempMask = np.clip(m, 0, 255).astype('uint8')
                image = Image.fromarray(tempMask.squeeze()).convert('L')
                image.save(mask_dir+"/" + str(count) + "_" + str(xSize) + "-" + str(ySize) + "-" + str(i).replace(".", "dot") + "_" + str(j).replace(".", "dot") + ".png")
                count+=1

def create_polygon_minmax_points_dict(polygons):
    polygon_minmax_points_dict = {}
    for each_poly in polygons:
        polygon_minmax_points_dict[tuple(each_poly)] = find_bottom_right_top_left(each_poly)
    return polygon_minmax_points_dict


xSize = 64 #101
ySize = 64 #101

x = [28.0680318]
y = [38.5714250]

createImageAndPatches("./bugday_patches", "./bugday_masks", BUGDAY_SHP_FILE_PATH, xSize, ySize, x, y)
