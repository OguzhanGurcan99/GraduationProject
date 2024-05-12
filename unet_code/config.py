import os
from read_mt_data import prefix

DATASET_PATH = "C:/Users/oguzh/PycharmProjects/graduationProject/data"
IMAGE_DATASET_PATH = os.path.join(DATASET_PATH, "patches/"+prefix+"_patches")
MASK_DATASET_PATH = os.path.join(DATASET_PATH, "masks/"+prefix+"_masks")
TEST_SPLIT = 0.15
DEVICE = "cpu"
PIN_MEMORY = True if DEVICE == "cuda" else False

INIT_LR = 0.001
NUM_EPOCHS = 8
BATCH_SIZE = 12
INPUT_IMAGE_WIDTH = 64
INPUT_IMAGE_HEIGHT = 64
THRESHOLD = 0.3
BASE_OUTPUT = "C:/Users/oguzh/PycharmProjects/graduationProject/"+prefix+"_output"
MODEL_PATH = os.path.join(BASE_OUTPUT, prefix+"_model.pth")
PLOT_PATH = os.path.sep.join([BASE_OUTPUT, prefix+"_plot.png"])
TEST_PATHS = os.path.sep.join([BASE_OUTPUT, prefix+"_test_paths.txt"])


