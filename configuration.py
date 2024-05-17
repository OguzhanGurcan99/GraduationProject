import colorsys

BUGDAY_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\bugday.shp"
DOMATES_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\domates.shp"
MISIR_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\misir.shp"
MISIR2_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\misir2.shp"
PAMUK_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\pamuk.shp"
UZUM_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\uzum.shp"
YONCA_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\yonca.shp"
ZEYTIN_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\zeytin.shp"

BUGDAY_OUTPUT_MAP_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\probs\\bugday_probs_0.png"
DOMATES_OUTPUT_MAP_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\probs\\domates_probs_0.png"
MISIR_OUTPUT_MAP_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\probs\\misir_probs_0.png"
MISIR2_OUTPUT_MAP_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\probs\\misir2_probs_0.png"
PAMUK_OUTPUT_MAP_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\probs\\pamuk_probs_0.png"
UZUM_OUTPUT_MAP_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\probs\\uzum_probs_0.png"
YONCA_OUTPUT_MAP_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\probs\\yonca_probs_0.png"
ZEYTIN_OUTPUT_MAP_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\probs\\zeytin_probs_0.png"


COORDINATES_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\coordinates.txt"

_04_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\04_VH.tif"
_04_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\04_VV.tif"
_04_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\04_VV-VH.tif"

_05_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\05_VH.tif"
_05_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\05_VV.tif"
_05_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\05_VV-VH.tif"

_06_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\06_VH.tif"
_06_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\06_VV.tif"
_06_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\06_VV-VH.tif"

_07_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\07_VH.tif"
_07_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\07_VV.tif"
_07_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\07_VV-VH.tif"

_08_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\08_VH.tif"
_08_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\08_VV.tif"
_08_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\08_VV-VH.tif"

_09_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\09_VH.tif"
_09_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\09_VV.tif"
_09_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\09_VV-VH.tif"

_10_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\10_VH.tif"
_10_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\10_VV.tif"
_10_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\10_VV-VH.tif"


CROP_COLOR_CODES = {
    "bugday" : (255,149,0),
    "domates" : (212,255,0),
    "misir" : (64,255,0),
    "misir2" : (0,255,234),
    "pamuk" : (0,127,255),
    "uzum" : (21,0,255),
    "yonca" : (255,0,191),
    "zeytin" : (255,0,43),
    "diger" : (0,0,0)
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
