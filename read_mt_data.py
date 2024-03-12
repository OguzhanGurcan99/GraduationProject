import geopandas as gpd
import utm
from shapely.geometry import Point, Polygon
import rasterio
import numpy as np
import cv2

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

def cutPatchAndCreateMask(raster, xSize, ySize, startX, startY, polygons):
    rasterMap = np.random.randint(255, size=(xSize, ySize))
    rasterMask = np.random.randint(255, size=(xSize, ySize))
    for i in range(startX, startX+xSize):
        for j in range(startY, startY+ySize):
            rasterMap[i-startX][j-startY]=raster.read(1)[i][j]
            val = raster.xy(i, j)
            lat, lon = utm.to_latlon(val[0], val[1], 35, northern=True)
            point = Point(lat, lon)
            flag = True
            for k in polygons:
                poly = Polygon(k)
                result = isPointInsidePolygon(point, poly)
                if result:
                    flag = False
                    rasterMask[i-startX][j-startY] = 255
                    break
            if flag:
                rasterMask[i-startX][j-startY] = 0

    cv2.imwrite("image" + str(xSize) + "-" + str(ySize) + "-" + str(startX) + "-" + str(startY) + ".png", rasterMap)
    cv2.imwrite("mask" + str(xSize) + "-" + str(ySize) + "-" + str(startX) + "-" + str(startY) + ".png", rasterMask)


bugday_polygons = read_shp_file("C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\mt_data\\01_Train_Test_Shapefile\\00_Train\\bugday.shp")

rasterVH = rasterio.open("C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\mt_data\\VH.tif")
rasterVV = rasterio.open("C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\mt_data\\VV.tif")
rasterVVVH = rasterio.open("C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\mt_data\\VV-VH.tif")

xSize = 101
ySize = 101
startX = 400
startY = 1700

ct=0
for i in range(300, 700, 200):
    for j in range(1500, 1900, 200):
        cutPatchAndCreateMask(rasterVH, 101, 101, i, j, bugday_polygons)
        print(ct)
        ct+=1

#cutPatchAndCreateMask(rasterVH, xSize, ySize, startX, startY, bugday_polygons)
