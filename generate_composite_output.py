import cv2
from PIL import Image
import configuration

bugday_probs = cv2.imread(configuration.BUGDAY_OUTPUT_MAP_PATH, cv2.IMREAD_GRAYSCALE)
domates_probs = cv2.imread(configuration.DOMATES_OUTPUT_MAP_PATH, cv2.IMREAD_GRAYSCALE)
misir_probs = cv2.imread(configuration.MISIR_OUTPUT_MAP_PATH, cv2.IMREAD_GRAYSCALE)
misir2_probs = cv2.imread(configuration.MISIR2_OUTPUT_MAP_PATH, cv2.IMREAD_GRAYSCALE)
pamuk_probs = cv2.imread(configuration.PAMUK_OUTPUT_MAP_PATH, cv2.IMREAD_GRAYSCALE)
uzum_probs = cv2.imread(configuration.UZUM_OUTPUT_MAP_PATH, cv2.IMREAD_GRAYSCALE)
yonca_probs = cv2.imread(configuration.YONCA_OUTPUT_MAP_PATH, cv2.IMREAD_GRAYSCALE)
zeytin_probs = cv2.imread(configuration.ZEYTIN_OUTPUT_MAP_PATH, cv2.IMREAD_GRAYSCALE)

def generate_image(W, H):
    return Image.new("RGB", (W, H))

def assign_pixel(img, x, y, color):
    img.putpixel((x, y), color)

width = 64
height = 64
image = generate_image(width, height)

for i in range(width):
    for j in range(height):
        bugday_pixel = True if bugday_probs is not None and bugday_probs[i][j] == 255 else False
        domates_pixel = True if domates_probs is not None and domates_probs[i][j] == 255 else False
        misir_pixel = True if misir_probs is not None and misir_probs[i][j] == 255 else False
        misir2_pixel = True if misir2_probs is not None and misir2_probs[i][j] == 255 else False
        pamuk_pixel = True if pamuk_probs is not None and pamuk_probs[i][j] == 255 else False
        uzum_pixel = True if uzum_probs is not None and uzum_probs[i][j] == 255 else False
        yonca_pixel = True if yonca_probs is not None and yonca_probs[i][j] == 255 else False
        zeytin_pixel = True if zeytin_probs is not None and zeytin_probs[i][j] == 255 else False

        if bugday_pixel:
            assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['bugday'])
        elif domates_pixel:
            assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['domates'])
        elif misir_pixel:
            assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['misir'])
        elif misir2_pixel:
            assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['misir2'])
        elif pamuk_pixel:
            assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['pamuk'])
        elif uzum_pixel:
            assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['uzum'])
        elif yonca_pixel:
            assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['yonca'])
        elif zeytin_pixel:
            assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['zeytin'])
        else:
            assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['diger'])


image = image.rotate(90)
image = image.transpose(Image.FLIP_TOP_BOTTOM)
image.save("generated_image.png")
