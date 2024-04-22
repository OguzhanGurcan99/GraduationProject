BUGDAY_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\mt_data\\01_Train_Test_Shapefile\\00_Train\\bugday.shp"
DOMATES_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\mt_data\\01_Train_Test_Shapefile\\00_Train\\domates.shp"
MISIR_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\mt_data\\01_Train_Test_Shapefile\\00_Train\\misir.shp"
MISIR2_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\mt_data\\01_Train_Test_Shapefile\\00_Train\\misir2.shp"
PAMUK_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\mt_data\\01_Train_Test_Shapefile\\00_Train\\pamuk.shp"
UZUM_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\mt_data\\01_Train_Test_Shapefile\\00_Train\\uzum.shp"
YONCA_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\mt_data\\01_Train_Test_Shapefile\\00_Train\\yonca.shp"
ZEYTIN_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\mt_data\\01_Train_Test_Shapefile\\00_Train\\zeytin.shp"

COORDINATES_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\coordinates.txt"

_04_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\04_VH.tif"
_04_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\04_VV.tif"
_04_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\04_VV-VH.tif"

_05_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\05_VH.tif"
_05_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\05_VV.tif"
_05_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\05_VV-VH.tif"

_06_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\06_VH.tif"
_06_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\06_VV.tif"
_06_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\06_VV-VH.tif"

_07_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\07_VH.tif"
_07_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\07_VV.tif"
_07_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\07_VV-VH.tif"

_08_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\08_VH.tif"
_08_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\08_VV.tif"
_08_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\08_VV-VH.tif"

_09_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\09_VH.tif"
_09_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\09_VV.tif"
_09_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\09_VV-VH.tif"

_10_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\10_VH.tif"
_10_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\10_VV.tif"
_10_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\10_VV-VH.tif"

CROP_COLOR_CODES = {
    "bugday" : (255,0,0),   #red
    "domates" : (0,255,0),  #green
    "misir" : (0,0,255),    #blue
    "misir2" : (0,0,255),    #blue
    "pamuk" : (128,0,128),  #purple
    "uzum" : (128,128,0),   #olive
    "yonca" : (0,255,255),  #aqua
    "zeytin" : (255,127,80),#coral
    "diger" : (0,0,0)       #black
}

class_map = {
    (255, 0, 0): 0,
    (0, 255, 0): 1,
    (0, 0, 255): 2,
    (128,0,128): 3,
    (128,128,0): 4,
    (0,255,255): 5,
    (255,127,80): 6,
    (0,0,0): 7
}

class_map_reverse = {
    0 : (255, 0, 0),
    1 : (0, 255, 0),
    2 : (0, 0, 255),
    3 : (128,0,128),
    4 : (128,128,0),
    5 : (0,255,255),
    6 : (255,127,80),
    7 : (0,0,0)
}
