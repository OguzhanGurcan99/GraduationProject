from PIL.Image import Image
from sklearn.metrics import confusion_matrix

from unet_code import config
import matplotlib.pyplot as plt
import numpy as np
import torch
import cv2
import os

def create_file_if_not_exist(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(file_path):
        with open(file_path, 'a+'):
            pass

def calculate_iou(mask1, mask2):
    mask1 = mask1.astype(bool)
    mask2 = mask2.astype(bool)
    intersection = np.logical_and(mask1, mask2)
    union = np.logical_or(mask1, mask2)
    iou = np.sum(intersection) / np.sum(union)
    return iou

def calculate_dice_coefficient(mask1, mask2):
    mask1 = mask1.astype(bool)
    mask2 = mask2.astype(bool)
    intersection = np.logical_and(mask1, mask2)
    intersection_count = np.count_nonzero(intersection)
    mask1_count = np.count_nonzero(mask1)
    mask2_count = np.count_nonzero(mask2)
    dice_coefficient = (2.0 * intersection_count) / (mask1_count + mask2_count)
    return dice_coefficient

def prepare_plot(origImage, origMask, predMask, ct, filename, patch_identifier):
    figure, ax = plt.subplots(nrows=1, ncols=3, figsize=(10, 10))
    ax[0].imshow(origImage)
    ax[1].imshow(origMask)
    ax[2].imshow(predMask)
    ax[0].set_title("Image")
    ax[1].set_title("Original Mask")
    ax[2].set_title("Predicted Mask")
    figure.suptitle(filename)
    figure.tight_layout()
    figure.savefig("plot_"+patch_identifier+'.png')
    #figure.show()


def make_predictions(model, imagePath, ct):
    model.eval()
    with torch.no_grad():
        numpy_array = np.load(imagePath)
        image = torch.tensor(numpy_array, dtype=torch.float32)
        filename = imagePath.split(os.path.sep)[-1].replace("npy", "png")
        groundTruthPath = os.path.join(config.MASK_DATASET_PATH, filename)
        gtMask = cv2.imread(groundTruthPath, 0)
        gtMask = torch.tensor(gtMask, dtype=torch.float32)
        image = image.unsqueeze(0)
        predMask = model(image)
        predMask = predMask.squeeze()
        output_probs = torch.sigmoid(predMask)
        output_probs_np = output_probs.cpu().numpy()
        output_probs_np = (output_probs_np > config.THRESHOLD) * 255
        output_probs_np = output_probs_np.astype(np.uint8)
        ones_array = np.mean(numpy_array, axis=0)
        patch_identifier = imagePath.split("\\")[-1].split(".")[0]
        prepare_plot(ones_array, gtMask, output_probs_np, ct, filename, patch_identifier)
        conf_matrix = confusion_matrix(gtMask.flatten(), output_probs_np.flatten())
        print(conf_matrix)
        print("-----")
        '''
        TP = conf_matrix[0][0]
        FP = conf_matrix[0][1]
        FN = conf_matrix[1][0]
        TN = conf_matrix[1][1]
        #print(TP + "_" + FP + "_" + FN + "_" + TN)
        print("ACCURACY: ", (TP+TN)/(TP+FP+TN+FN))
        print("IOU: ", calculate_iou(output_probs_np, gtMask.numpy()))
        print("DICE: ",calculate_dice_coefficient(output_probs_np, gtMask.numpy()))
        '''
        subfolder = 'probs'
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        cv2.imwrite(os.path.join(subfolder, config.prefix+'_probs_' + patch_identifier + '.png'), output_probs_np)
        create_file_if_not_exist(config.PROBS_FILE_PATH)
        with open(config.PROBS_FILE_PATH, 'a+') as destination:
            destination.write(patch_identifier+"\n")

imagePaths = open(config.TEST_PATHS).read().strip().split("\n")
imagePaths = np.random.choice(imagePaths, size=3)

unet = torch.load(config.MODEL_PATH).to(config.DEVICE)

ct=0
for path in imagePaths:
    make_predictions(unet, path, ct)
    ct+=1
