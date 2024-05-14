import geopandas as gpd
import utm
from PIL import Image
from shapely.geometry import Point, Polygon
import rasterio
import numpy as np
import os
import configuration
from configuration import *

def create_file_if_not_exist(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(file_path):
        with open(file_path, 'a+'):
            pass
def save_coordinates(source_file, destination_file):
    create_file_if_not_exist(destination_file)
    with open(source_file, 'r') as source:
        with open(destination_file, 'a+') as destination:
            destination.write(source.read())
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
def createImageAndPatches(patch_dir, mask_dir, shapefile_path, xSize, ySize, coordinates_list, rasters):
    createDirectoriesIfNotExist([patch_dir, mask_dir])
    polygons = read_shp_file(shapefile_path)
    min_max_points = create_polygon_minmax_points_dict(polygons)

    #row, col = raster1.index(x[0], y[0])
    #val = raster1.xy(450, 1610)
    #crs_x, crs_y = raster1.xy(880, 2140)
    #pixel_value = raster1.read(1)[row, col]

    count=0
    for pair in coordinates_list:
        count+=1
        print("Image " + str(count) + " Processing...")
        i = pair[0]
        j = pair[1]
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

        #save only first mask, bc all of them are same
        tempMask = np.clip(rasterMasks[0], 0, 255).astype('uint8')
        image = Image.fromarray(tempMask.squeeze()).convert('L')
        image.save(mask_dir+"/" + str(xSize) + "-" + str(ySize) + "-" + str(i).replace(".", "dot") + "_" + str(j).replace(".", "dot") + ".png")
def create_polygon_minmax_points_dict(polygons):
    polygon_minmax_points_dict = {}
    for each_poly in polygons:
        polygon_minmax_points_dict[tuple(each_poly)] = find_bottom_right_top_left(each_poly)
    return polygon_minmax_points_dict
def readCoordinatesFromFile(file_path, points):
    file = open(file_path, "r")
    for line in file.readlines():
        xValue = float(line.split(",")[1].rstrip())
        yValue = float(line.split(",")[0])
        points.append([xValue, yValue])
    return points



rasters = [
        rasterio.open(configuration._04_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._04_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._04_VV_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._05_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._05_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._05_VV_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._06_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._06_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._06_VV_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._07_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._07_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._07_VV_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._08_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._08_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._08_VV_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._09_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._09_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._09_VV_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._10_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._10_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._10_VV_VH_TIFF_FILE_PATH)
    ]

#PARAMETERS
#PARAMETERS
xSize = 64 #101
ySize = 64 #101

prefix = "misir" # TODO patch, mask uretimi ve train-predict asamalarinda guncellenmeli.
shp_file_path = MISIR_SHP_FILE_PATH
#PARAMETERS
#PARAMETERS


coordinates_list = readCoordinatesFromFile(COORDINATES_FILE_PATH, [])
createImageAndPatches("./data/patches/"+prefix+"_patches", "./data/masks/"+prefix+"_masks", shp_file_path, xSize, ySize, coordinates_list, rasters)
save_coordinates(COORDINATES_FILE_PATH, "./data/"+prefix+"_samples.txt")
